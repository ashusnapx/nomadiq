"""Destination Research Agent finding relevant attractions using hybrid RAG context."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class DestinationResearchAgent(BaseAgent):
    """Retrieves target sights, activities, and dining places matching interests."""

    name: str = "DestinationResearchAgent"
    prompt_category: str = "system"
    prompt_name: str = "destination_research"
    complexity: TaskComplexity = TaskComplexity.COMPLEX


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=DestinationResearchAgent.name,
        agent_class=DestinationResearchAgent,
        prompt_category=DestinationResearchAgent.prompt_category,
        prompt_name=DestinationResearchAgent.prompt_name,
        version="v1",
        complexity=DestinationResearchAgent.complexity,
    )
)
