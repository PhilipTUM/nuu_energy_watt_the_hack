"""Calculate exactly one metric: heat_load_consumption."""

from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule


class ConsumptionHeatLoadModule(MetricModule):
    """Derive heat_load_consumption without making an investment decision."""

    output_key = "heat_load_consumption"
    requires = ("space_heating_demand",)

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(
        self, user_input: UserInput, previous_results: CalculationOutput
    ) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        return self.available(
            previous_results.space_heating_demand.value / self.config.full_load_hours,
            "kW",
            (
                f"{self.config.full_load_hours:g} Volllaststunden pro Jahr; keine Norm-Heizlast.",
            ),
        )
