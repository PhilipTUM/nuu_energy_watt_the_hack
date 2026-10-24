"""Extract cached German TABULA reference data; requires openpyxl only for import.

Usage: python tools/import_tabula.py --source-root <project folder>
Runtime uses the resulting JSON and Python standard library only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import openpyxl


def extract(root):
    """Read source values without recalculating or modifying the workbooks."""
    result_path = root / 'TABULA-Analyses_DE-Typology_DataTables/TABULA-Analyses_DE-Typology_ResultData.xlsx'
    climate_path = root / 'tabula-calculator.xlsx'
    workbook = openpyxl.load_workbook(result_path, read_only=True, data_only=True)
    sheet = workbook['Values Output.Set.1 DE-All']
    rows = list(sheet.values)
    header = rows[0]
    profiles = {}
    mapping = {'type_code': 'Code_BuildingType', 'size_class': 'Code_BuildingSizeClass',
               'year_from': 'Year1_Building', 'year_to': 'Year2_Building',
               'reference_area_m2': 'A_C_Ref', 'living_area_m2': 'A_C_Living',
               'h_transmission_w_m2k': 'h_Transmission', 'h_ventilation_w_m2k': 'h_Ventilation',
               'heating_need_kwh_m2a': 'q_h_nd', 'variant_kind': 'Code_TypeVariant'}
    for number, row in enumerate(rows[10:], 11):
        record = dict(zip(header, row))
        code = record['Code_BuildingVariant']
        if not isinstance(code, str) or not code.startswith('DE.') or not code.endswith(('.001', '.002', '.003')):
            continue
        profile = {key: record[source] for key, source in mapping.items()}
        if code in profiles:
            previous = {key: profiles[code][key] for key in mapping}
            if previous != profile:
                raise ValueError('Inconsistent duplicate profile: ' + code)
            continue
        assert profile['reference_area_m2'] > 0 and profile['living_area_m2'] > 0
        assert profile['h_transmission_w_m2k'] > 0 and profile['h_ventilation_w_m2k'] >= 0
        profile['source_row'] = number
        profile['code'] = code
        # Reproduce the transmission coefficient from the individual element terms.
        terms = [record[name] for name in header if str(name).startswith('H_Transmission_')]
        expected = sum(terms) / profile['reference_area_m2']
        if abs(expected - profile['h_transmission_w_m2k']) > 1e-8:
            raise ValueError('Transmission reconciliation failed: ' + code)
        profiles[code] = profile
    workbook.close()
    workbook = openpyxl.load_workbook(climate_path, read_only=True, data_only=True)
    sheet = workbook['Tab.AuxCalc.Climate']
    rows = list(sheet.values)
    header = rows[0]
    climates = {}
    for number, row in enumerate(rows[10:], 11):
        d = dict(zip(header, row))
        code = d['Code_ClimateRegion']
        if not isinstance(code, str) or not (code.startswith('DE.KR') or code == 'DE.N'):
            continue
        climates[code] = {'code': code, 'name': d['Name_ClimateRegion_National'], 'source_row': number,
                         'remarks': d['Remarks'],
                         'temperatures_c': [d[f'theta_e_{m:02}'] for m in range(1, 13)],
                         'solar_daily_kwh_m2': {direction: [d[f'I_Sol_{direction}_{m:02}'] for m in range(1, 13)]
                                                for direction in ('North', 'East', 'South', 'West')}}
    workbook.close()
    return {'schema_version': 1,
            'sources': [{'file': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in (result_path, climate_path)],
            'profiles': dict(sorted(profiles.items())), 'climates': dict(sorted(climates.items()))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    args = parser.parse_args()
    data = extract(args.source_root)
    target = Path(__file__).resolve().parents[1] / 'heat_pump_ready/data/tabula_de.json'
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Imported {len(data['profiles'])} profiles and {len(data['climates'])} climates into {target}")
