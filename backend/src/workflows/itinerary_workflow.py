"""LangGraph workflow orchestrating travel compilation agents in sequence."""

from __future__ import annotations

import logging
from typing import Any, TypedDict
from langgraph.graph import StateGraph, END

from backend.src.integrations.model_router import ModelRouter
from backend.src.agents.user_preference import UserPreferenceAgent
from backend.src.agents.destination_research import DestinationResearchAgent
from backend.src.agents.weather_intelligence import WeatherIntelligenceAgent
from backend.src.agents.transportation import TransportationAgent
from backend.src.agents.optimization import OptimizationAgent
from backend.src.agents.safety import SafetyAgent
from backend.src.agents.summary import SummaryAgent

logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """Execution state passed between LangGraph agent nodes."""

    trip_input: dict[str, Any]
    preferences: dict[str, Any]
    research: list[dict[str, Any]]
    weather: dict[str, Any]
    transport: dict[str, Any]
    optimized_plans: dict[str, Any]
    safety: dict[str, Any]
    summary: dict[str, Any]
    traces: list[dict[str, Any]]
    errors: list[str]


class ItineraryWorkflow:
    """Orchestrates multi-agent trip compilation using LangGraph state machine."""

    def __init__(self, router: ModelRouter) -> None:
        self._router = router
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        builder = StateGraph(WorkflowState)

        # Add Nodes
        builder.add_node("extract_preferences", self._node_preferences)
        builder.add_node("research_destination", self._node_research)
        builder.add_node("analyze_weather", self._node_weather)
        builder.add_node("plan_transport", self._node_transport)
        builder.add_node("optimize_budget", self._node_optimize)
        builder.add_node("verify_safety", self._node_safety)
        builder.add_node("summarize", self._node_summary)

        # Add Edges
        builder.set_entry_point("extract_preferences")
        builder.add_edge("extract_preferences", "research_destination")
        builder.add_edge("research_destination", "analyze_weather")
        builder.add_edge("analyze_weather", "plan_transport")
        builder.add_edge("plan_transport", "optimize_budget")
        builder.add_edge("optimize_budget", "verify_safety")
        builder.add_edge("verify_safety", "summarize")
        builder.add_edge("summarize", END)

        return builder.compile()

    async def execute(self, trip_input: dict[str, Any]) -> dict[str, Any]:
        """Run the multi-agent graph with initial inputs."""
        init_state: WorkflowState = {
            "trip_input": trip_input,
            "preferences": {},
            "research": [],
            "weather": {},
            "transport": {},
            "optimized_plans": {},
            "safety": {},
            "summary": {},
            "traces": [],
            "errors": [],
        }
        return await self._graph.ainvoke(init_state)

    # Nodes Implementations
    async def _node_preferences(self, state: WorkflowState) -> dict:
        agent = UserPreferenceAgent(self._router)
        res = await agent.run(
            user_input=state["trip_input"].get("preferences_text", ""),
            destination=state["trip_input"].get("destination", ""),
            start_date=state["trip_input"].get("start_date", ""),
            end_date=state["trip_input"].get("end_date", ""),
            budget_min=state["trip_input"].get("budget_min", 0.0),
            budget_max=state["trip_input"].get("budget_max", 1000.0),
            persona=state["trip_input"].get("persona", "Balanced"),
        )
        return {
            "preferences": res.data,
            "traces": [self._trace_map(res)],
        }

    async def _node_research(self, state: WorkflowState) -> dict:
        agent = DestinationResearchAgent(self._router)
        res = await agent.run(
            destination=state["trip_input"].get("destination", ""),
            start_date=state["trip_input"].get("start_date", ""),
            end_date=state["trip_input"].get("end_date", ""),
            budget_min=state["trip_input"].get("budget_min", 0.0),
            budget_max=state["trip_input"].get("budget_max", 1000.0),
            persona=state["trip_input"].get("persona", "Balanced"),
            preferences=state["preferences"],
            retrieved_context="Grounded recommendations for sightseeing, dining and landmarks.",
            min_activities=2,
            max_activities=4,
        )
        return {
            "research": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    async def _node_weather(self, state: WorkflowState) -> dict:
        agent = WeatherIntelligenceAgent(self._router)
        res = await agent.run(
            destination=state["trip_input"].get("destination", ""),
            start_date=state["trip_input"].get("start_date", ""),
            end_date=state["trip_input"].get("end_date", ""),
            weather_data="Sunny weather expected across travel dates.",
            planned_activities=state["research"],
        )
        return {
            "weather": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    async def _node_transport(self, state: WorkflowState) -> dict:
        agent = TransportationAgent(self._router)
        res = await agent.run(
            destination=state["trip_input"].get("destination", ""),
            activities=state["research"],
            transport_modes="Walking, Public Transit, Taxi",
            transport_budget_pct=15,
            walk_threshold_km=2.0,
            max_walk_km=10.0,
            mobility_requirements="None",
            transport_budget=100.0,
        )
        return {
            "transport": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    async def _node_optimize(self, state: WorkflowState) -> dict:
        agent = OptimizationAgent(self._router)
        res = await agent.run(
            current_itinerary=state["research"],
            budget_min=state["trip_input"].get("budget_min", 0.0),
            budget_max=state["trip_input"].get("budget_max", 1000.0),
            current_cost=150.0,
            budget_utilization=15,
            preferences=state["preferences"],
            destination=state["trip_input"].get("destination", ""),
            persona=state["trip_input"].get("persona", "Balanced"),
        )
        return {
            "optimized_plans": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    async def _node_safety(self, state: WorkflowState) -> dict:
        agent = SafetyAgent(self._router)
        res = await agent.run(
            itinerary=state["optimized_plans"],
            destination=state["trip_input"].get("destination", ""),
            persona=state["trip_input"].get("persona", "Balanced"),
            preferences=state["preferences"],
        )
        return {
            "safety": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    async def _node_summary(self, state: WorkflowState) -> dict:
        agent = SummaryAgent(self._router)
        res = await agent.run(
            destination=state["trip_input"].get("destination", ""),
            start_date=state["trip_input"].get("start_date", ""),
            end_date=state["trip_input"].get("end_date", ""),
            persona=state["trip_input"].get("persona", "Balanced"),
            budget_min=state["trip_input"].get("budget_min", 0.0),
            budget_max=state["trip_input"].get("budget_max", 1000.0),
            itinerary_data=state["optimized_plans"],
            weather_summary=state["weather"],
            transport_summary=state["transport"],
            safety_notes=state["safety"],
            citations=["Retrieved Travel Guidebook"],
        )
        return {
            "summary": res.data,
            "traces": state["traces"] + [self._trace_map(res)],
        }

    def _trace_map(self, res: Any) -> dict:
        import datetime
        return {
            "agent_name": res.agent_name,
            "model_used": res.model_used,
            "tokens": res.tokens,
            "latency_ms": res.latency_ms,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
overrides = {}
