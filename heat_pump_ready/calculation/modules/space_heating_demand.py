"""Calculate exactly one metric: space_heating_demand."""

from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule


class SpaceHeatingDemandModule(MetricModule):
    """Derive space_heating_demand without making an investment decision."""

    output_key = "space_heating_demand"
    requires = ("useful_heat", "hot_water_demand")

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(
        self, user_input: UserInput, previous_results: CalculationOutput
    ) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        value = (
            previous_results.useful_heat.value - previous_results.hot_water_demand.value
        )
        return self.available(
            value,
            "kWh/a",
            ("Nutzwärme minus Warmwasser; negative Werte prüft der Validator.",),
        )
