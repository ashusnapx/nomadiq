"""Agent Registry enabling dynamic agent registration and discovery at startup."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Type
from backend.src.integrations.model_router import TaskComplexity

logger = logging.getLogger(__name__)


@dataclass
class AgentSpec:
    """Registration spec for an agent."""

    name: str
    agent_class: Type[Any]
    prompt_category: str
    prompt_name: str
    version: str
    complexity: TaskComplexity
    tools: list[str] = None


class AgentRegistry:
    """Central catalog for all agent implementations."""

    def __init__(self) -> None:
        self._registry: dict[str, AgentSpec] = {}

    def register(self, spec: AgentSpec) -> None:
        """Add an agent to the central catalog."""
        self._registry[spec.name] = spec
        logger.info(
            f"Successfully registered agent: {spec.name} (Complexity: {spec.complexity.value})"
        )

    def get(self, name: str) -> AgentSpec:
        """Retrieve registered agent specification by unique name."""
        if name not in self._registry:
            raise KeyError(f"Agent '{name}' is not registered in the catalog.")
        return self._registry[name]

    def list_agents(self) -> list[AgentSpec]:
        """List all currently registered agent configurations."""
        return list(self._registry.values())


agent_registry = AgentRegistry()
