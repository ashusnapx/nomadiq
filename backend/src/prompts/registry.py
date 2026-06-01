"""Prompt registry with versioning and loading capabilities."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.src.exceptions.agent_errors import PromptLoadError

_PROMPT_DIR = Path(__file__).parent / "templates"


class PromptVersion:
    """Tracks a single prompt version with metadata."""

    def __init__(self, name: str, content: str, version: str) -> None:
        self.name = name
        self.content = content
        self.version = version
        self.hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        self.loaded_at = datetime.now(timezone.utc)

    def render(self, **kwargs: Any) -> str:
        """Render prompt with variable substitution."""
        try:
            return self.content.format(**kwargs)
        except KeyError as exc:
            raise PromptLoadError(
                f"Missing variable {exc} in prompt '{self.name}'"
            ) from exc


class PromptRegistry:
    """Central registry for loading and managing prompts."""

    def __init__(self, prompt_dir: Path | None = None) -> None:
        self._dir = prompt_dir or _PROMPT_DIR
        self._cache: dict[str, PromptVersion] = {}

    def load(self, category: str, name: str, version: str = "v1") -> PromptVersion:
        """Load a prompt template by category and name."""
        cache_key = f"{category}/{name}/{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = self._dir / category / version / f"{name}.txt"
        if not path.exists():
            path = self._dir / category / f"{name}.txt"
        if not path.exists():
            raise PromptLoadError(f"Prompt not found: {path}")

        content = path.read_text(encoding="utf-8").strip()
        prompt = PromptVersion(name=name, content=content, version=version)
        self._cache[cache_key] = prompt
        return prompt

    def render(self, category: str, name: str, version: str = "v1", **kwargs: Any) -> str:
        """Load and render a prompt in one call."""
        return self.load(category, name, version).render(**kwargs)

    def list_prompts(self) -> list[dict[str, str]]:
        """List all loaded prompts with metadata."""
        return [
            {"name": p.name, "version": p.version, "hash": p.hash}
            for p in self._cache.values()
        ]

    def clear_cache(self) -> None:
        """Clear the prompt cache."""
        self._cache.clear()


prompt_registry = PromptRegistry()
