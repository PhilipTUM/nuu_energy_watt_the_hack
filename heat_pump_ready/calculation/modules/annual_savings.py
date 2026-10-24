"""Calculate exactly one metric: annual_savings."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class AnnualSavingsModule(MetricModule):
    """Derive annual_savings without making an investment decision."""
    output_key = 'annual_savings'
    requires = ('current_energy_cost', 'heat_pump_energy_cost')

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        return self.available(previous_results.current_energy_cost.value - previous_results.heat_pump_energy_cost.value, '€/a', ('Differenz der Energiekosten, ohne Wartung und Grundpreise.',))
