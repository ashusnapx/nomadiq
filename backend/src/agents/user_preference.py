"""User Preference Agent parsing traveler request into structured preference parameters."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class UserPreferenceAgent(BaseAgent):
    """Parses natural language trip requests and extracts traveler interests and constraints."""

    name: str = "UserPreferenceAgent"
    prompt_category: str = "system"
    prompt_name: str = "user_preference"
    complexity: TaskComplexity = TaskComplexity.SIMPLE


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=UserPreferenceAgent.name,
        agent_class=UserPreferenceAgent,
        prompt_category=UserPreferenceAgent.prompt_category,
        prompt_name=UserPreferenceAgent.prompt_name,
        version="v1",
        complexity=UserPreferenceAgent.complexity,
    )
)
