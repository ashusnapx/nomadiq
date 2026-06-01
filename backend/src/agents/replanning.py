"""Replanning Agent selectively regenerating slots affected by active events."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class ReplanningAgent(BaseAgent):
    """Surgically replaces disrupted elements while leaving non-impacted slots intact."""

    name: str = "ReplanningAgent"
    prompt_category: str = "replanning"
    prompt_name: str = "replan"
    complexity: TaskComplexity = TaskComplexity.COMPLEX


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=ReplanningAgent.name,
        agent_class=ReplanningAgent,
        prompt_category=ReplanningAgent.prompt_category,
        prompt_name=ReplanningAgent.prompt_name,
        version="v1",
        complexity=ReplanningAgent.complexity,
    )
)
overrides = {}
