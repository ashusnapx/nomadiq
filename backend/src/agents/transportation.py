"""Transportation Agent calculating optimal routes and travel durations."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class TransportationAgent(BaseAgent):
    """Calculates geographical distances and transit segments between activities."""

    name: str = "TransportationAgent"
    prompt_category: str = "system"
    prompt_name: str = "transportation"
    complexity: TaskComplexity = TaskComplexity.MODERATE


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=TransportationAgent.name,
        agent_class=TransportationAgent,
        prompt_category=TransportationAgent.prompt_category,
        prompt_name=TransportationAgent.prompt_name,
        version="v1",
        complexity=TransportationAgent.complexity,
    )
)
