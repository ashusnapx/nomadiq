"""Base AI Agent class orchestrating LLM queries and token cost registrations."""

from __future__ import annotations

import abc
import time
import json
import logging
from typing import Any
from backend.src.integrations.model_router import ModelRouter, TaskComplexity
from backend.src.prompts.registry import prompt_registry

logger = logging.getLogger(__name__)


class AgentResult:
    """Standardized output structure for single agent invocations."""

    def __init__(
        self,
        data: dict,
        agent_name: str,
        model_used: str,
        tokens: dict,
        latency_ms: float,
    ) -> None:
        self.data = data
        self.agent_name = agent_name
        self.model_used = model_used
        self.tokens = tokens
        self.latency_ms = latency_ms


class BaseAgent(abc.ABC):
    """Abstract Base Agent providing template resolution, model routing, and timers."""

    name: str = "BaseAgent"
    prompt_category: str = "system"
    prompt_name: str = "base"
    complexity: TaskComplexity = TaskComplexity.SIMPLE

    def __init__(self, router: ModelRouter) -> None:
        self._router = router

    async def run(self, **kwargs: Any) -> AgentResult:
        """Execute agent workflow node."""
        start = time.perf_counter()
        prompt = self._load_prompt(**kwargs)

        messages = [{"role": "system", "content": prompt}]
        if user_msg := kwargs.get("user_message"):
            messages.append({"role": "user", "content": user_msg})

        # Call the Model Router
        result = await self._router.invoke(
            messages=messages,
            complexity=self.complexity,
            response_format={"type": "json_object"},
        )

        latency = (time.perf_counter() - start) * 1000
        parsed_data = self._parse_response(result["content"])

        return AgentResult(
            data=parsed_data,
            agent_name=self.name,
            model_used=result["model"],
            tokens=result["usage"],
            latency_ms=latency,
        )

    def _load_prompt(self, **kwargs: Any) -> str:
        """Resolve and format prompt template from registry."""
        return prompt_registry.render(
            category=self.prompt_category, name=self.prompt_name, **kwargs
        )

    def _parse_response(self, content: str) -> dict:
        """Safely parse JSON outputs with error fallbacks."""
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.error(
                f"Agent '{self.name}' response is not valid JSON: {exc}. Raw: {content}"
            )
            return {"error": "Invalid response format", "raw": content}
overrides = {}
