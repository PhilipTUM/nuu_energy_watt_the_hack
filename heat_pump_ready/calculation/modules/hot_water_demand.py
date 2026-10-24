"""Calculate exactly one metric: hot_water_demand."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class HotWaterDemandModule(MetricModule):
    """Derive hot_water_demand without making an investment decision."""
    output_key = 'hot_water_demand'
    requires = ()

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        if user_input.hot_water_via_heating is False:
            return self.available(0.0, 'kWh/a', ('Warmwasser wird separat erzeugt.',))
        if user_input.hot_water_via_heating is None or user_input.persons_in_household is None:
            return self.missing('Warmwasserbereitung und Personenanzahl fehlen.')
        return self.available(user_input.persons_in_household * self.config.hot_water_kwh_per_person, 'kWh/a', (f'{self.config.hot_water_kwh_per_person:g} kWh Warmwasser pro Person und Jahr (Challenge-Annahme).',), demonstration=True)
