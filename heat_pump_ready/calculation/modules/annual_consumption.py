"""Annual consumption is already supplied in kWh by the authorized CSV schema."""
from .base import MetricModule


class AnnualConsumptionModule(MetricModule):
    """Do not reconvert oil litres mentioned in a descriptive text field."""
    output_key = 'annual_consumption'
    requires = ()

    def __init__(self, runner, config):
        """Retain registry compatibility; CSV inputs need no LLM or conversion."""
        pass

    def calculate(self, user_input, previous_results):
        """Return the explicit annual_consumption_kwh column, including real zero."""
        if user_input.annual_consumption_kwh is None:
            return self.missing('annual_consumption_kwh ist in der CSV nicht dokumentiert.')
        return self.available(user_input.annual_consumption_kwh, 'kWh/a',
                              ('CSV-Spalte annual_consumption_kwh; bereits kWh, keine erneute Liter-/m³-Umrechnung.',))
