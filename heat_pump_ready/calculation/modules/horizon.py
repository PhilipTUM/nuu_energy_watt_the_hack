"""Calculate exactly one metric: horizon."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule

class HorizonModule(MetricModule):
    """Derive horizon without making an investment decision."""
    output_key = 'horizon'
    requires = ()

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        return self.available(user_input.horizon_years, 'Jahre', ('Vom Nutzer gewählter Betrachtungszeitraum.',))
