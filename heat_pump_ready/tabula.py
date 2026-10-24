"""Local TABULA reference ranges using only facts from the allowed CSV schema."""
from functools import lru_cache
from pathlib import Path
import json


@lru_cache(maxsize=1)
def catalog():
    """Load source values once; no workbook dependency at runtime."""
    return json.loads((Path(__file__).parent / 'data/tabula_de.json').read_text(encoding='utf-8'))


def matching_profiles(user_input):
    """Select German age-class scenarios, never infer an undocumented building type.

    Unknown/partial/full renovation cannot uniquely identify a TABULA package.
    Consequently all three source states remain scenarios. Explicitly unrenovated
    input limits the set to the source's first variant, without inventing type.
    """
    if user_input.construction_year is None or user_input.floor_area_m2 is None:
        return ()
    return tuple(profile for profile in catalog()['profiles'].values()
                 if profile['year_from'] <= user_input.construction_year <= profile['year_to']
                 and (user_input.renovation_status != 'unrenovated' or profile['code'].endswith('.001')))


def reference_area(user_input, profile):
    """Scale reference area by the source archetype's living-area ratio."""
    return user_input.floor_area_m2 * profile['reference_area_m2'] / profile['living_area_m2']


def scenario_range(user_input, column):
    """Return min/max values plus their source witnesses; never return a mean."""
    profiles = matching_profiles(user_input)
    if not profiles:
        return None
    values = [(profile[column] * reference_area(user_input, profile), profile) for profile in profiles]
    low = min(values, key=lambda pair: pair[0])
    high = max(values, key=lambda pair: pair[0])
    evidence = []
    for label, (value, profile) in (('Untergrenze', low), ('Obergrenze', high)):
        evidence.append(f"{label}: {profile['code']}, Zeile {profile['source_row']}, {column}={profile[column]:.6g}, "
                        f"A_C_Ref/A_C_Living={profile['reference_area_m2']:.6g}/{profile['living_area_m2']:.6g}; Ergebnis {value:.2f}.")
    return (low[0], high[0]), tuple(evidence), len(profiles)


def range_metric(module, user_input, column, unit, meaning):
    """Build one source-backed typology range with an explicit interpretation."""
    result = scenario_range(user_input, column)
    if result is None:
        return module.missing('Baujahr/Fläche fehlen oder Baujahr außerhalb der lokalen TABULA-Abdeckung; keine Typologie erfunden.')
    values, evidence, count = result
    return module.available(values, unit,
                            (meaning,
                             f'{count} passende deutsche Baualters-/Varianten-Szenarien; Gebäudetyp nicht dokumentiert, daher kein einzelnes Referenzhaus zugewiesen.',
                             'Beheizte CSV-Fläche als Wohnfläche interpretiert; pro Szenario A_C_Ref = Fläche × A_C_Ref/A_C_Living.',
                             'Ohne eindeutige Zuordnung bleiben Sanierungsvarianten Szenarien; keine Aussage über tatsächlich durchgeführte Maßnahmen.'),
                            ('TABULA-Analyses_DE-Typology_ResultData.xlsx, Values Output.Set.1 DE-All.',) + evidence,
                            demonstration=True,
                            uncertainty='Typologische Szenariospanne, kein Konfidenzintervall und keine berechnete Gebäude-Normbilanz. Wärmerückgewinnung nicht abgezogen.')
