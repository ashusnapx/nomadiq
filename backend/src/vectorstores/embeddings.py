"""Embedding service using OpenAI API with mock fallbacks."""

from __future__ import annotations

import logging
from openai import AsyncOpenAI
from backend.src.config.settings import get_settings
from backend.src.observability.cost_tracker import cost_tracker

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Generate embeddings via OpenAI with thread-safe cost tracking and mock fallbacks."""

    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.openai_api_key
        self._is_gemini = self._api_key.startswith("AIzaSy") if self._api_key else False
        
        if self._is_gemini:
            logger.info("Gemini API key detected. Configuring EmbeddingService for Google OpenAI-compatible endpoint.")
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self._model = "text-embedding-004"
        else:
            # Establish OpenAI client lazily only if api key is present
            self._client = AsyncOpenAI(api_key=self._api_key) if self._api_key else None
            self._model = settings.embedding_model

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text string, falling back to deterministic mock vectors if offline or on API failure."""
        if not self._client:
            logger.warning("No OpenAI key detected. Mocking text embedding vector offline.")
            return [0.01] * 1536

        try:
            response = await self._client.embeddings.create(
                model=self._model, input=text
            )
            usage = response.usage
            cost_tracker.record(
                model=self._model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=0,
            )
            return response.data[0].embedding
        except Exception as exc:
            logger.warning(f"Embedding API call failed: {exc}. Falling back to offline mock vectors.")
            return [0.01] * 1536

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts in a single API call, falling back to offline mocks on API failure."""
        if not texts:
            return []
        if not self._client:
            logger.warning("No OpenAI key detected. Mocking batch embedding vectors offline.")
            return [[0.01] * 1536 for _ in texts]

        try:
            response = await self._client.embeddings.create(
                model=self._model, input=texts
            )
            cost_tracker.record(
                model=self._model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=0,
            )
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [item.embedding for item in sorted_data]
        except Exception as exc:
            logger.warning(f"Embedding batch API call failed: {exc}. Falling back to offline mock vectors.")
            return [[0.01] * 1536 for _ in texts]


overrides = {}
