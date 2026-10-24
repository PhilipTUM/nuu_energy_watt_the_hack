"""Calculate exactly one metric: payback_period."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class PaybackPeriodModule(MetricModule):
    """Derive payback_period without making an investment decision."""
    output_key = 'payback_period'
    requires = ('annual_savings', 'net_investment')

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        savings = previous_results.annual_savings.value
        if savings <= 0:
            return self.available('no_finite_payback', 'Jahre', ('Keine positive jährliche Energiekostenersparnis.',), demonstration=True)
        return self.available(previous_results.net_investment.value / savings, 'Jahre', ('Einfache Amortisation ohne Zinsen, Wartung, Preisänderung und Ersatzinvestitionen.',), demonstration=True)
