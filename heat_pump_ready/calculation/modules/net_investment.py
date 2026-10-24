"""Calculate exactly one metric: net_investment."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class NetInvestmentModule(MetricModule):
    """Derive net_investment without making an investment decision."""
    output_key = 'net_investment'
    requires = ()

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        if user_input.investment_eur is None or user_input.subsidy_eur is None:
            return self.missing('Investitionskosten und Förderung fehlen; 0 € Förderung bitte ausdrücklich eingeben.')
        return self.available(user_input.investment_eur - user_input.subsidy_eur, '€', ('Vom Nutzer eingegebene Kosten und Förderung; keine Förderprüfung.',))
