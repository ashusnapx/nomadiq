"""What-If Simulation Service analyzing hypotheticals across variants."""

from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.workflows.simulation_workflow import SimulationWorkflow
from backend.src.integrations.model_router import ModelRouter
from backend.src.repositories.itinerary_repository import ItineraryRepository

logger = logging.getLogger(__name__)


class WhatIfService:
    """Invokes what-if simulations to analyze constraints and forecast variant impacts."""

    def __init__(self, db: AsyncSession) -> None:
        self._itinerary_repo = ItineraryRepository(db)
        self._router = ModelRouter()

    async def simulate_scenario(
        self, trip_id: int, scenario_type: str, parameter_value: str
    ) -> dict:
        """Apply simulated closures, cuts or delays across all trip variants."""
        variants = await self._itinerary_repo.get_by_trip(trip_id)

        # Map models to serialization dicts for workflow consumption
        vars_payload = []
        for var in variants:
            vars_payload.append(
                {
                    "variant": var.variant.value,
                    "confidence_score": var.confidence_score,
                    "total_cost": var.total_cost,
                    "activities": [
                        {"id": a.id, "name": a.name, "cost": a.cost, "day": a.day_number}
                        for a in var.activities
                    ],
                }
            )

        sim = SimulationWorkflow(self._router)
        res = await sim.execute(
            {
                "trip_id": trip_id,
                "scenario_type": scenario_type,
                "parameter_value": parameter_value,
                "variants": vars_payload,
            }
        )

        return {
            "trip_id": trip_id,
            "scenario": f"{scenario_type}: {parameter_value}",
            "results": res.get("results", []),
        }
overrides = {}
