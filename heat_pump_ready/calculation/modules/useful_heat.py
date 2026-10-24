"""Calculate exactly one metric: useful_heat."""

from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule


class UsefulHeatModule(MetricModule):
    """Derive useful_heat without making an investment decision."""

    output_key = "useful_heat"
    requires = ("annual_consumption",)

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(
        self, user_input: UserInput, previous_results: CalculationOutput
    ) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        if user_input.energy_carrier not in ("gas", "oil", "lpg"):
            return self.missing(
                "Nutzungsgrad für diesen Energieträger noch nicht definiert."
            )
        return self.available(
            previous_results.annual_consumption.value * self.config.boiler_efficiency,
            "kWh/a",
            (f"Kesselnutzungsgrad {self.config.boiler_efficiency:g} (Konfiguration).",),
        )
