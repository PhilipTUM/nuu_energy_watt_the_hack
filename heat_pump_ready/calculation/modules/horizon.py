"""A user-selected investment horizon is absent from the authorized CSV."""
from .base import MetricModule


class HorizonModule(MetricModule):
    """Do not introduce a new financial input under the CSV-only contract."""
    output_key = 'horizon'
    requires = ()

    def __init__(self, config):
        """Retain registry compatibility."""
        pass

    def calculate(self, user_input, previous_results):
        """Missing horizon is unavailable, rather than an invented twenty years."""
        return self.missing('Betrachtungszeitraum nicht in buildings_eval.csv enthalten.')
