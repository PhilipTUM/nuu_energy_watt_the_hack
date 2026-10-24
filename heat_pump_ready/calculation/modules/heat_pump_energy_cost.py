"""Calculate exactly one metric: heat_pump_energy_cost."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class HeatPumpEnergyCostModule(MetricModule):
    """Derive heat_pump_energy_cost without making an investment decision."""
    output_key = 'heat_pump_energy_cost'
    requires = ('useful_heat', 'annual_performance_factor')

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        value = previous_results.useful_heat.value / previous_results.annual_performance_factor.value * self.config.hp_price_eur_kwh
        return self.available(value, '€/a', (f'Strom {self.config.hp_price_eur_kwh:g} €/kWh; gleicher Wärmelieferumfang inklusive bisher zentralem Warmwasser.',))
