"""Extract a radiator type only when it is explicitly documented in radiator_info."""
import re
from .base import MetricModule


class RadiatorTypeModule(MetricModule):
    """A documented type is not a measurement of radiator dimensions or output."""
    output_key = 'radiator_type'
    requires = ()

    def __init__(self, runner):
        """Registry compatibility; no image fields exist in the CSV schema."""
        pass

    def calculate(self, user_input, previous_results):
        """Recognize explicit type 11/22/33; avoid counting radiator quantities."""
        types = set(re.findall(r'\b(?:type|typ)\s*[:=]?\s*(11|22|33)\b', user_input.radiator_info, re.IGNORECASE))
        if len(types) != 1:
            return self.missing('Heizkörpertyp 11/22/33 nicht eindeutig dokumentiert. Maße und Nennleistung fehlen; keine Leistungsdeckung ableitbar.')
        return self.available(next(iter(types)), evidence=('Explizite Typangabe in radiator_info; gilt nicht automatisch für alle Heizkörper.',),
                              uncertainty='Ohne Maße, Nennleistung und Raumheizlast keine Dimensionierung bei 55 °C möglich.')
