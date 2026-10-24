"""Investment is not an input column in buildings_eval.csv."""
from .base import MetricModule


class NetInvestmentModule(MetricModule):
    """Do not invent costs or subsidies from typology or energy consumption."""
    output_key = 'net_investment'
    requires = ()

    def __init__(self, config):
        """Retain registry compatibility without adding input fields."""
        pass

    def calculate(self, user_input, previous_results):
        """Return an explicit information gap under the CSV-only contract."""
        return self.missing('Investitionskosten und Förderung sind keine Spalten der zugelassenen CSV; Nettoinvestition und Amortisation bleiben offen.')
