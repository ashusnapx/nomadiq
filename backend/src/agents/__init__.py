"""Agents package exporting base agent and auto-registering implementations."""

from __future__ import annotations

from backend.src.agents.base import BaseAgent, AgentResult
from backend.src.agents.registry import agent_registry, AgentSpec

# Explicit imports to trigger auto-registration hooks
from backend.src.agents.user_preference import UserPreferenceAgent
from backend.src.agents.destination_research import DestinationResearchAgent
from backend.src.agents.weather_intelligence import WeatherIntelligenceAgent
from backend.src.agents.transportation import TransportationAgent
from backend.src.agents.optimization import OptimizationAgent
from backend.src.agents.safety import SafetyAgent
from backend.src.agents.replanning import ReplanningAgent
from backend.src.agents.summary import SummaryAgent

__all__ = [
    "BaseAgent",
    "AgentResult",
    "agent_registry",
    "AgentSpec",
    "UserPreferenceAgent",
    "DestinationResearchAgent",
    "WeatherIntelligenceAgent",
    "TransportationAgent",
    "OptimizationAgent",
    "SafetyAgent",
    "ReplanningAgent",
    "SummaryAgent",
]
