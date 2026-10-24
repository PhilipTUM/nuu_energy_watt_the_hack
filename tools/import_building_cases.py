"""Package local Notion cases using only the evaluation input schema.

Run from repository root: python -m tools.import_building_cases --source-root ../..
"""
import argparse
import csv
from pathlib import Path
from heat_pump_ready.intake import INPUT_COLUMNS, build_user_input


def import_cases(source_root):
    """Verify eval schema; exclude dev labels before writing packaged snapshots."""
    output = Path(__file__).resolve().parents[1] / 'heat_pump_ready/data'
    for name in ('buildings_dev.csv', 'buildings_eval.csv'):
        source = source_root / 'Data_Notion' / name
        with source.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if name == 'buildings_eval.csv' and tuple(reader.fieldnames) != INPUT_COLUMNS:
                raise ValueError('Evaluation source columns differ from the authorized input contract')
            rows = [{key: row.get(key, '') for key in INPUT_COLUMNS} for row in reader]
        for row in rows:
            build_user_input(row)
        with (output / name).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=INPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        print(f'{name}: {len(rows)} cases, {len(INPUT_COLUMNS)} input columns; references excluded')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    args = parser.parse_args()
    import_cases(args.source_root)
