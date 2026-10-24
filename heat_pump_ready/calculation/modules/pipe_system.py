"""Determine one pipe-system category from user input or image evidence."""

from ...contracts import UserInput, CalculationOutput, MetricResult
from .extraction import ExtractionModule


class PipeSystemModule(ExtractionModule):
    """Do not infer a two-pipe system merely from two visible radiator connections."""

    output_key = "pipe_system"
    requires = ()

    def calculate(
        self, user_input: UserInput, previous_results: CalculationOutput
    ) -> MetricResult:
        """Return supplied pipe system or uncertain structured image observation."""
        if user_input.pipe_system != "unknown":
            return self.available(
                user_input.pipe_system, evidence=("Explizite Nutzerangabe.",)
            )
        images = [file for file in user_input.attachments if file.category == "pipes"]
        return self.extract(
            images,
            "Rohrsystem: single-pipe oder two-pipe. Zwei Anschlüsse oder H-Blöcke allein beweisen nichts; dann null. Beschreibe sichtbare Belege.",
            ("single-pipe", "two-pipe"),
        )
