"""Independent annual TABULA heating-need scenarios, never fuel consumption."""
from .base import MetricModule
from ...tabula import range_metric


class TabulaSpaceHeatingDemandModule(MetricModule):
    """Keep the source climate and energy-reference area of q_h_nd explicit."""
    output_key = 'tabula_space_heating_demand'
    requires = ()

    def calculate(self, user_input, previous_results):
        """Do not divide annual energy by a temperature to fabricate a peak load."""
        return range_metric(self, user_input, 'heating_need_kwh_m2a', 'kWh/a',
                            'q_h_nd × übertragene A_C_Ref; ursprüngliches TABULA-Rechenklima, vor systemseitiger Wärmerückgewinnung. Reine Raumwärme, weder Brennstoffverbrauch noch Heizlast; keine PLZ-Klimakorrektur.')
