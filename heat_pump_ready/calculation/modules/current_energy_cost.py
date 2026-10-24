"""Calculate exactly one metric: current_energy_cost."""
from ...config import AssessmentConfig
from ...contracts import UserInput, CalculationOutput, MetricResult
from .base import MetricModule
from ..fuels import resolved_carrier

class CurrentEnergyCostModule(MetricModule):
    """Derive current_energy_cost without making an investment decision."""
    output_key = 'current_energy_cost'
    requires = ('annual_consumption',)

    def __init__(self, config: AssessmentConfig) -> None:
        """Store validated calculation configuration; no IO is performed."""
        self.config = config

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return one metric from input and declared prior metrics; inputs stay unchanged."""
        prices = {'gas': self.config.gas_price_eur_kwh, 'oil': self.config.oil_price_eur_kwh}
        carrier = resolved_carrier(user_input)
        if carrier not in prices:
            return self.missing('Kein vorgegebener Vergleichstarif für diesen Energieträger.')
        price = prices[carrier]
        return self.available(previous_results.annual_consumption.value * price, '€/a', (f'Brennstoffpreis {price:.2f} €/kWh; feste Challenge-Vorgabe; nur Energiebezug.',), demonstration=True)
