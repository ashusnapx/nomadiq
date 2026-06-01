"""Safety Agent assessing travel risks, scam spots, and emergency contacts."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class SafetyAgent(BaseAgent):
    """Audits planned activities against safety limits, advising traveler of emergency rules."""

    name: str = "SafetyAgent"
    prompt_category: str = "safety"
    prompt_name: str = "safety_review"
    complexity: TaskComplexity = TaskComplexity.SIMPLE


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=SafetyAgent.name,
        agent_class=SafetyAgent,
        prompt_category=SafetyAgent.prompt_category,
        prompt_name=SafetyAgent.prompt_name,
        version="v1",
        complexity=SafetyAgent.complexity,
    )
)
