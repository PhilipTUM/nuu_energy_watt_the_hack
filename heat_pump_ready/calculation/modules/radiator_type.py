"""Extract a single radiator type only when one radiator image is supplied."""
from ...contracts import UserInput, CalculationOutput, MetricResult
from .extraction import ExtractionModule

class RadiatorTypeModule(ExtractionModule):
    """A pictured radiator does not describe every radiator in the building."""
    output_key = 'radiator_type'
    requires = ()

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Return type 11/22/33 for one pictured radiator; ambiguous sets stay unknown."""
        images = [file for file in user_input.attachments if file.category == 'radiator']
        if len(images) > 1:
            return self.missing('Für diese Kennzahl bitte genau ein repräsentatives Heizkörperfoto wählen.')
        return self.extract(images, 'Heizkörpertyp: 11, 22 oder 33 als String, nur bei sichtbaren Platten/Konvektorlagen. Kein Rückschluss auf Größe oder ausreichende Leistung.', ('11', '22', '33'))
