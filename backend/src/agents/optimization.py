"""Optimization Agent producing Plan A, B, and C variants matching budget profiles."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent
from backend.src.agents.registry import AgentSpec, agent_registry
from backend.src.integrations.model_router import TaskComplexity


class OptimizationAgent(BaseAgent):
    """Refines activities to construct high-value balanced, budget, and luxury plans."""

    name: str = "OptimizationAgent"
    prompt_category: str = "system"
    prompt_name: str = "optimization"
    complexity: TaskComplexity = TaskComplexity.COMPLEX


# Auto-register at load time
agent_registry.register(
    AgentSpec(
        name=OptimizationAgent.name,
        agent_class=OptimizationAgent,
        prompt_category=OptimizationAgent.prompt_category,
        prompt_name=OptimizationAgent.prompt_name,
        version="v1",
        complexity=OptimizationAgent.complexity,
    )
)
