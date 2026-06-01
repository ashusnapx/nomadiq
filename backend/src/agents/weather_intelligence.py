"""Weather Intelligence Agent scoring activity feasibility under forecast conditions."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class WeatherIntelligenceAgent(BaseAgent):
    """Evaluates forecast parameters and maps weather suitability scores to scheduled plans."""

    name: str = "WeatherIntelligenceAgent"
    prompt_category: str = "system"
    prompt_name: str = "weather_intelligence"
    complexity: TaskComplexity = TaskComplexity.SIMPLE


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=WeatherIntelligenceAgent.name,
        agent_class=WeatherIntelligenceAgent,
        prompt_category=WeatherIntelligenceAgent.prompt_category,
        prompt_name=WeatherIntelligenceAgent.prompt_name,
        version="v1",
        complexity=WeatherIntelligenceAgent.complexity,
    )
)
