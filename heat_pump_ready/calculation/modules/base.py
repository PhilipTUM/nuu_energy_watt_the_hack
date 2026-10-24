"""Small shared result constructors for metric modules, without decision logic."""
from ...contracts import MetricResult

class MetricModule:
    """Common naming and provenance helpers; subclasses implement one calculation."""
    output_key = ''
    requires = ()

    @property
    def name(self):
        """Return the stable module identifier."""
        return type(self).__name__

    def available(self, value, unit=None, assumptions=(), evidence=(), demonstration=False, uncertainty=None):
        """Create one available metric with explicit assumptions and evidence."""
        return MetricResult(self.output_key, 'available', value, unit, self.name,
                            tuple(assumptions), tuple(evidence), uncertainty, demonstration)

    def missing(self, reason):
        """Return unavailable metric without substituting zero."""
        return MetricResult(self.output_key, 'missing_input', source=self.name, evidence=(reason,))
