"""Actual local Notion CSV cases, restricted to the evaluation input schema."""
import csv
from pathlib import Path


def load_cases():
    """Read packaged CSV snapshots; dev reference labels have been excluded."""
    cases = []
    for name in ('buildings_dev.csv', 'buildings_eval.csv'):
        with (Path(__file__).parent / 'data' / name).open(encoding='utf-8', newline='') as stream:
            cases.extend(dict(row) for row in csv.DictReader(stream))
    return cases


CASES = load_cases()
SYNTHETIC = {'building_id': 'DEMO', 'construction_year': 2005, 'floor_area_m2': 180,
             'renovation_status': 'fully', 'annual_consumption_kwh': 24000,
             'energy_carrier': 'gas', 'energy_carrier_detail': 'natural gas',
             'persons_in_household': 3, 'hot_water_via_heating': True,
             'heat_distribution': 'radiators', 'pipe_system': 'two-pipe', 'flow_temperature_c': 50,
             'radiator_info': '', 'rooms': None, 'location': '',
             'building_notes': 'Synthetisches Beispiel innerhalb des CSV-Schemas; kein nuuEnergy-Referenzgebäude.'}
