from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any, TypeAlias

import gc

import mlx.core as mx
from huggingface_hub.utils import disable_progress_bars
from mlx_vlm import load, stream_generate
from mlx_vlm.prompt_utils import apply_chat_template
from PIL.Image import Image as PILImage

from app_logging.logger import Logger

disable_progress_bars()


PreparedImage: TypeAlias = PILImage


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerationOptions:

    max_tokens: int = 5_000
    temperature: float = 0.2
    enable_thinking: bool = False
    thinking_budget: int | None = None

    # Gemma-4-Tokens statt Qwen-Tokens <think>...</think>
    thinking_start_token: str = "<|think|>"
    thinking_end_token: str = "<channel|>"

    def __post_init__(self) -> None:
        # Checks später ergänzen
        pass

    def to_mlx_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "enable_thinking": self.enable_thinking,
        }

        if self.enable_thinking:
            kwargs["thinking_start_token"] = self.thinking_start_token
            kwargs["thinking_end_token"] = self.thinking_end_token

            if self.thinking_budget is not None:
                kwargs["thinking_budget"] = self.thinking_budget

        return kwargs


class GEMMA_4_12B:

    def __init__(self, logger: Logger | None = None) -> None:
        self._model_id = "mlx-community/gemma-4-12B-it-4bit"
        self._logger = logger
        self._model: Any | None = None
        self._processor: Any | None = None

        self.load()

    def load(self) -> None:
        if self._model is not None and self._processor is not None:
            self._log("Model is already loaded")
            return

        self._log(f"Loading model {self._model_id!r}")

        self._model, self._processor = load(self._model_id)

        # Kein zusätzliches mx.eval(...) erforderlich:
        # mlx_vlm.load(..., lazy=False) materialisiert das Modell bereits.

        self._log(
            f"Model initialized and ready – using "
            f"{self.active_memory_gib:.2f} GiB active memory"
        )

    @property
    def active_memory_gib(self) -> float:
        return mx.get_active_memory() / 1024**3

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def model(self) -> Any:
        return self._model

    @property
    def processor(self) -> Any:
        return self._processor

    def generate(
        self,
        prompt: str,
        *,
        images: Sequence[PreparedImage] | None = None,
        options: GenerationOptions | None = None,
    ) -> Iterator[str]:
        options = options or GenerationOptions()

        # mlx-vlm erwartet für mehrere Bilder zuverlässig eine Liste.
        image_list = list(images) if images is not None else None
        img_cnt = len(image_list) if image_list else 0

        formatted_prompt = apply_chat_template(
            self._processor,
            self._model.config,
            prompt,
            num_images=img_cnt,
            enable_thinking=options.enable_thinking,
        )

        self._log(
            f"Generating response with {img_cnt} image(s) – "
            f"{self.active_memory_gib:.2f} GiB active memory"
        )

        for chunk in stream_generate(
            model=self._model,
            processor=self._processor,
            prompt=formatted_prompt,
            image=image_list or None,
            **options.to_mlx_kwargs(),
        ):
            if chunk.text:
                yield chunk.text

    def _log(self, message: str) -> None:
        if self._logger is not None:
            self._logger.info(message)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" f"model_id={self._model_id!r})"

    def unload(self) -> None:
        memory_before = self.active_memory_gib

        mx.synchronize()

        self._model = None
        self._processor = None

        gc.collect()
        mx.clear_cache()

        self._log(
            f"Model unloaded – active memory: "
            f"{memory_before:.2f} → {self.active_memory_gib:.2f} GiB"
        )
