"""Simulation Engine comparing hypothetical what-if scenarios across variants."""

from __future__ import annotations

import logging
from typing import Any, TypedDict
from langgraph.graph import StateGraph, END

from backend.src.integrations.model_router import ModelRouter
from backend.src.agents.replanning import ReplanningAgent

logger = logging.getLogger(__name__)


class SimulationState(TypedDict):
    """Internal state passed during What-If simulation execution."""

    trip_id: int
    scenario_type: str
    parameter_value: str
    variants: list[dict[str, Any]]
    results: list[dict[str, Any]]
    traces: list[dict[str, Any]]
    errors: list[str]


class SimulationWorkflow:
    """Simulates rain/budget reductions/closures and generates comparison scoreboards."""

    def __init__(self, router: ModelRouter) -> None:
        self._router = router
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        builder = StateGraph(SimulationState)

        # Single step simulation node
        builder.add_node("simulate_scenario", self._node_simulate)

        builder.set_entry_point("simulate_scenario")
        builder.add_edge("simulate_scenario", END)

        return builder.compile()

    async def execute(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Run the What-If simulation workflow graph."""
        init_state: SimulationState = {
            "trip_id": inputs["trip_id"],
            "scenario_type": inputs["scenario_type"],
            "parameter_value": inputs["parameter_value"],
            "variants": inputs["variants"],
            "results": [],
            "traces": [],
            "errors": [],
        }
        return await self._graph.ainvoke(init_state)

    async def _node_simulate(self, state: SimulationState) -> dict:
        results = []
        agent = ReplanningAgent(self._router)

        for var in state["variants"]:
            # Simulate impact of scenario on specific variant
            res = await agent.run(
                event_type=state["scenario_type"],
                severity="warning",
                event_description=f"What-If Simulation: {state['parameter_value']}",
                affected_time="Simulation Day",
                affected_location="Simulation Area",
                current_itinerary=var,
                impact_analysis="Hypothetical scenario simulation",
                affected_activities=var.get("activities", [])[:1],  # Mock first activity as affected
                budget_remaining=var.get("total_cost", 1000.0) * 0.8,
                preferences={},
            )

            modified = res.data.get("modified_activities", [])
            orig_cost = var.get("total_cost", 500.0)
            cost_delta = res.data.get("cost_delta", 0.0)

            results.append(
                {
                    "variant_name": var.get("variant", "Plan A"),
                    "original_cost": orig_cost,
                    "simulated_cost": orig_cost + cost_delta,
                    "original_score": var.get("confidence_score", 0.9),
                    "simulated_score": res.data.get("confidence", 0.8),
                    "affected_activities": [
                        act.get("name", "Activity")
                        for act in var.get("activities", [])[:1]
                    ],
                    "replacements": [act.get("name", "New Activity") for act in modified],
                }
            )

        return {"results": results}
overrides = {}
