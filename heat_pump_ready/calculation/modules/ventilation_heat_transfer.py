"""Gross ventilation loss scenarios before system-side heat recovery."""
from .base import MetricModule
from ...tabula import range_metric


class VentilationHeatTransferModule(MetricModule):
    """Return typological H_V range rather than inventing air-change rates."""
    output_key = 'ventilation_heat_transfer'
    requires = ()

    def calculate(self, user_input, previous_results):
        """The CSV cannot identify airtightness or a heat-recovery system."""
        return range_metric(self, user_input, 'h_ventilation_w_m2k', 'W/K',
                            'H_V = h_Ventilation × übertragene A_C_Ref; getrennt von Transmission wie in ISO 52016-1, 6.6.6. Vor systemseitiger Wärmerückgewinnung.')
