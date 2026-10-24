"""Structural contract for one-metric calculation modules."""
from typing import Protocol, Tuple
from ..contracts import UserInput, CalculationOutput, MetricResult

class CalculationModule(Protocol):
    """A module reads immutable snapshots and returns exactly its declared metric."""
    name: str
    output_key: str
    requires: Tuple[str, ...]

    def calculate(self, user_input: UserInput, previous_results: CalculationOutput) -> MetricResult:
        """Calculate one metric without mutating input, output or global configuration."""
        ...
