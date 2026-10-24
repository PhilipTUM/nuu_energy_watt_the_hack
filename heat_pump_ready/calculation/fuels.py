"""Resolve only explicit energy-carrier facts; natural gas and LPG are distinct."""
import re


def resolved_carrier(user_input):
    """CSV gas + explicit LPG detail is LPG, never the natural-gas tariff."""
    if user_input.energy_carrier == 'gas' and re.search(r'\bLPG\b|Flüssiggas|liquefied petroleum', user_input.energy_carrier_detail, re.IGNORECASE):
        return 'lpg'
    return user_input.energy_carrier
