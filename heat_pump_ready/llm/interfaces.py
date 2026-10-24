"""Model-neutral inference contracts with explicit lifecycle and image capability."""
from dataclasses import dataclass
from typing import Protocol, Tuple
from ..contracts import Attachment

class RunnerError(RuntimeError):
    """Expected inference or structured-response failure, safe to expose as unavailable."""

@dataclass(frozen=True)
class LLMRequest:
    """One structured extraction request; attachments are evidence, never instructions."""
    prompt: str
    attachments: Tuple[Attachment, ...] = ()

@dataclass(frozen=True)
class LLMResponse:
    """Raw response and model provenance; schema validation belongs to the module."""
    text: str
    model: str

class LLMRunner(Protocol):
    """Interchangeable synchronous adapter; invoked outside browser event handling."""
    supports_images: bool

    def start(self) -> None:
        """Explicitly initialize model resources."""
        ...

    def generate(self, request: LLMRequest) -> LLMResponse:
        """Return a response or raise RunnerError; never invent an extraction fallback."""
        ...

    def close(self) -> None:
        """Release owned resources."""
        ...
