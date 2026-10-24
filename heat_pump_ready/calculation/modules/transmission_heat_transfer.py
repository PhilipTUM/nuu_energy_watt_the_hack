"""Transmission loss scenarios scaled from TABULA's German age classes."""
from .base import MetricModule
from ...tabula import range_metric


class TransmissionHeatTransferModule(MetricModule):
    """Return a typological H_T range in W/K with existing thermal bridges."""
    output_key = 'transmission_heat_transfer'
    requires = ()

    def calculate(self, user_input, previous_results):
        """Keep source envelope/ground adjustments and thermal bridges together."""
        return range_metric(self, user_input, 'h_transmission_w_m2k', 'W/K',
                            'H_T = h_Transmission × übertragene A_C_Ref; Wärmebrücken und TABULA-Bauteilkorrekturen enthalten. Bilanzstruktur nach ISO 52016-1, 6.6.5; keine Einzelbauteilberechnung.')
