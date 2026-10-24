"""Show disagreement between independent heat-load methods without averaging."""
from .base import MetricModule


class HeatLoadRangeModule(MetricModule):
    """Combine both estimates into a transparent envelope, not a confidence band."""
    output_key = 'heat_load_range'
    requires = ('heat_load_consumption', 'heat_load_area')

    def calculate(self, user_input, previous_results):
        """Retain the lowest/highest available method endpoints."""
        consumption = previous_results.heat_load_consumption.value
        area = previous_results.heat_load_area.value
        endpoints = area if isinstance(area, tuple) else (area,)
        values = (consumption,) + endpoints
        return self.available((min(values), max(values)), 'kW',
                              ('Spanne beider Heizlastmethoden; kein Mittelwert, kein statistisches Konfidenzintervall.',),
                              uncertainty='Methodenabweichungen bleiben sichtbar und müssen fachlich geklärt werden.')
