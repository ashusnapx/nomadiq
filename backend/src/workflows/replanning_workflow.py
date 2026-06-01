"""LangGraph workflow for dynamic event-driven itinerary replanning."""

from __future__ import annotations

import logging
from typing import Any, TypedDict
from langgraph.graph import StateGraph, END

from backend.src.integrations.model_router import ModelRouter
from backend.src.agents.replanning import ReplanningAgent

logger = logging.getLogger(__name__)


class ReplanningState(TypedDict):
    """Internal state passed during selective replanning execution."""

    trip_id: int
    event: dict[str, Any]
    current_itinerary: dict[str, Any]
    affected_activities: list[dict[str, Any]]
    budget_remaining: float
    preferences: dict[str, Any]
    replanned_activities: list[dict[str, Any]]
    explanation: str
    traces: list[dict[str, Any]]
    errors: list[str]


class ReplanningWorkflow:
    """Manages surgical regenerations of trip timelines affected by active events."""

    def __init__(self, router: ModelRouter) -> None:
        self._router = router
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        builder = StateGraph(ReplanningState)

        # Single step surgical replan node
        builder.add_node("surgical_replan", self._node_surgical_replan)

        builder.set_entry_point("surgical_replan")
        builder.add_edge("surgical_replan", END)

        return builder.compile()

    async def execute(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Run the selective replanning workflow state machine."""
        init_state: ReplanningState = {
            "trip_id": inputs["trip_id"],
            "event": inputs["event"],
            "current_itinerary": inputs["current_itinerary"],
            "affected_activities": inputs["affected_activities"],
            "budget_remaining": inputs.get("budget_remaining", 500.0),
            "preferences": inputs.get("preferences", {}),
            "replanned_activities": [],
            "explanation": "",
            "traces": [],
            "errors": [],
        }
        return await self._graph.ainvoke(init_state)

    async def _node_surgical_replan(self, state: ReplanningState) -> dict:
        agent = ReplanningAgent(self._router)
        res = await agent.run(
            event_type=state["event"].get("event_type", "General"),
            severity=state["event"].get("severity", "warning"),
            event_description=state["event"].get("description", ""),
            affected_time="Day Schedule",
            affected_location="Trip Area",
            current_itinerary=state["current_itinerary"],
            impact_analysis="Disruptions detected in travel routes.",
            affected_activities=state["affected_activities"],
            budget_remaining=state["budget_remaining"],
            preferences=state["preferences"],
        )
        return {
            "replanned_activities": res.data.get("modified_activities", []),
            "explanation": res.data.get("explanation", "Replanning completed."),
            "traces": [
                {
                    "agent_name": res.agent_name,
                    "model_used": res.model_used,
                    "tokens": res.tokens,
                    "latency_ms": res.latency_ms,
                }
            ],
        }
overrides = {}
