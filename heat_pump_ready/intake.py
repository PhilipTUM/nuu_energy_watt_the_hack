"""Validate exactly the input columns of buildings_eval.csv, including CSV blanks."""
import math
from dataclasses import fields
from datetime import date
from .contracts import UserInput

INPUT_COLUMNS = tuple(field.name for field in fields(UserInput))
ENUMS = {
    'renovation_status': ('unknown', 'unrenovated', 'partially', 'fully', 'low_energy'),
    'energy_carrier': ('gas', 'oil', 'lpg', 'district', 'electric'),
    'heat_distribution': ('unknown', 'radiators', 'underfloor', 'mixed'),
    'pipe_system': ('unknown', 'single-pipe', 'two-pipe'),
}
BOUNDS = {
    'construction_year': (1700, date.today().year), 'floor_area_m2': (1, 10000),
    'annual_consumption_kwh': (0, 10000000), 'persons_in_household': (0, 100),
    'flow_temperature_c': (10, 100), 'rooms': (1, 1000),
}
INTEGER_FIELDS = ('construction_year', 'persons_in_household', 'rooms')
TEXT_FIELDS = ('building_id', 'energy_carrier_detail', 'radiator_info', 'building_notes', 'location')


def build_user_input(payload: dict) -> UserInput:
    """Accept CSV strings or typed JSON; reject extra input variables explicitly."""
    if not isinstance(payload, dict):
        raise ValueError('Eingabe muss ein JSON-Objekt sein.')
    extra = set(payload) - set(INPUT_COLUMNS)
    if extra:
        raise ValueError('Nicht im CSV-Eingabeschema: ' + ', '.join(sorted(extra)))
    values = {}
    for key, (low, high) in BOUNDS.items():
        raw = payload.get(key)
        if raw is None or raw == '':
            continue
        if isinstance(raw, bool):
            raise ValueError(key + ': Zahl erwartet.')
        try:
            value = float(raw)
        except (TypeError, ValueError) as error:
            raise ValueError(key + ': Zahl erwartet.') from error
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f'{key}: Wert muss zwischen {low} und {high} liegen.')
        if key in INTEGER_FIELDS and not value.is_integer():
            raise ValueError(key + ': Ganze Zahl erwartet.')
        values[key] = int(value) if key in INTEGER_FIELDS else value
    for key, allowed in ENUMS.items():
        raw = payload.get(key)
        if raw is None or raw == '':
            continue
        if not isinstance(raw, str) or raw not in allowed:
            raise ValueError(key + ': Unbekannte Auswahl.')
        values[key] = raw
    hot_water = payload.get('hot_water_via_heating')
    if isinstance(hot_water, str):
        choices = {'': None, 'yes': True, 'no': False, 'true': True, 'false': False}
        if hot_water.lower() not in choices:
            raise ValueError('Warmwasser muss yes/no, true/false oder leer sein.')
        hot_water = choices[hot_water.lower()]
    if hot_water is not None and type(hot_water) is not bool:
        raise ValueError('Warmwasser muss true, false oder null sein.')
    values['hot_water_via_heating'] = hot_water
    for key in TEXT_FIELDS:
        raw = payload.get(key, '')
        if not isinstance(raw, str) or len(raw) > 4000:
            raise ValueError(key + ': Ungültiger Text.')
        values[key] = raw
    # The source labels LPG as gas plus an explicit fuel detail; preserve the
    # original columns and resolve that distinction only in calculation helpers.
    return UserInput(**values)
