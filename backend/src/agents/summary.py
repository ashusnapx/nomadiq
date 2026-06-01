"""Summary Agent producing polished traveler itinerary documents."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class SummaryAgent(BaseAgent):
    """Compiles structured plans, weather, and transport charts into formatted traveler text."""

    name: str = "SummaryAgent"
    prompt_category: str = "planner"
    prompt_name: str = "summary"
    complexity: TaskComplexity = TaskComplexity.MODERATE


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=SummaryAgent.name,
        agent_class=SummaryAgent,
        prompt_category=SummaryAgent.prompt_category,
        prompt_name=SummaryAgent.prompt_name,
        version="v1",
        complexity=SummaryAgent.complexity,
    )
)
overrides = {}
