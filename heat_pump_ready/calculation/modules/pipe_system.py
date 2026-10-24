"""Use only the explicit CSV pipe-system field; valves are not a system proof."""
from .base import MetricModule


class PipeSystemModule(MetricModule):
    """Unknown stays unknown; radiator blocks or construction year do not prove it."""
    output_key = 'pipe_system'
    requires = ()

    def __init__(self, runner):
        """Registry compatibility; this CSV-only module performs no inference."""
        pass

    def calculate(self, user_input, previous_results):
        """Return the documented pipe system without interpreting missing data."""
        if user_input.pipe_system == 'unknown':
            return self.missing('Rohrsystem nicht dokumentiert; Ventilblöcke und zwei Anschlüsse allein sind kein Nachweis.')
        return self.available(user_input.pipe_system, evidence=('Explizite CSV-Angabe pipe_system.',))
