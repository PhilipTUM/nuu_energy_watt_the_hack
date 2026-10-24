"""Calculate exactly one metric: heat_load_area."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class AreaHeatLoadModule(MetricModule):
    """Derive heat_load_area without making an investment decision."""
    output_key = 'heat_load_area'
    requires = ()

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        area, year, renovation = user_input.floor_area_m2, user_input.construction_year, user_input.renovation_status
        if area is None:
            return self.missing('Beheizte Fläche fehlt.')
        demo = False
        if renovation == 'low_energy':
            low, high = 15, 40
        elif renovation == 'fully' or (year is not None and year >= 2002):
            low, high = 40, 60
        elif year is not None and year < 1979 and renovation == 'unrenovated':
            low, high = 120, 180
        elif year is not None and 1980 <= year <= 1999 and renovation == 'unrenovated':
            low, high = 80, 120
        elif year is not None:
            low, high, demo = 40, 180, True
        else:
            return self.missing('Baujahr oder eindeutige Gebäudeklasse fehlt.')
        return self.available((area * low / 1000, area * high / 1000), 'kW', (f'{low}–{high} W/m²; grobe Gebäudeklasse.',), demonstration=True, uncertainty='Breite Demonstrationsspanne bei ungeklärter Gebäudeklasse.' if demo else 'Grobe Challenge-Richtwerte, keine Norm-Heizlast und keine TABULA-Gebäudezuweisung.')
