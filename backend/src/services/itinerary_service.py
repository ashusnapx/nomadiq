"""Itinerary Service driving the LangGraph compiler and database storage of plan variants."""

from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.itinerary import Itinerary
from backend.src.models.activity import Activity
from backend.src.domain.enums import PlanVariant
from backend.src.workflows.itinerary_workflow import ItineraryWorkflow
from backend.src.integrations.model_router import ModelRouter
from backend.src.repositories.itinerary_repository import ItineraryRepository
from backend.src.repositories.trip_repository import TripRepository
from backend.src.exceptions.api_errors import NotFoundError

logger = logging.getLogger(__name__)


class ItineraryService:
    """Invokes LangGraph workflows and serializes generated plan variants A/B/C."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._itinerary_repo = ItineraryRepository(db)
        self._trip_repo = TripRepository(db)
        self._router = ModelRouter()

    async def generate_itineraries(self, trip_id: int) -> list[Itinerary]:
        """Trigger LangGraph pipeline and persist three Plan A/B/C variants."""
        trip = await self._trip_repo.get_by_id(trip_id)
        if not trip:
            raise NotFoundError(f"Trip with ID {trip_id} not found.")

        # Trigger Workflow Orchestrator
        workflow = ItineraryWorkflow(self._router)
        res = await workflow.execute(
            {
                "destination": trip.destination,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "budget_min": trip.budget_min,
                "budget_max": trip.budget_max,
                "persona": trip.persona.value,
                "preferences_text": str(trip.preferences),
            }
        )

        variants = []
        # Parse and save Plan A, Plan B, Plan C
        plan_data = res.get("optimized_plans", {})

        for variant_enum in [PlanVariant.A, PlanVariant.B, PlanVariant.C]:
            # Default fallback data if agent misses variant keys
            v_name = variant_enum.value
            v_info = plan_data.get(v_name, plan_data.get(variant_enum.name, {}))

            cost = v_info.get("cost", trip.budget_min + 100.0)
            score = v_info.get("confidence", 0.9)

            itinerary = Itinerary(
                trip_id=trip_id,
                variant=variant_enum,
                confidence_score=score,
                total_cost=cost,
                is_active=(variant_enum == PlanVariant.A),  # Plan A active by default
            )
            await self._itinerary_repo.create(itinerary)

            # Persist activities
            raw_acts = v_info.get("activities", res.get("research", []))
            for idx, act in enumerate(raw_acts):
                activity = Activity(
                    itinerary_id=itinerary.id,
                    day_number=act.get("day", 1),
                    time_slot=act.get("best_time", "Morning"),
                    name=act.get("name", f"Landmark Walk {idx}"),
                    description=act.get("description", act.get("why_recommended", "Recreations.")),
                    location=act.get("location", trip.destination),
                    cost=act.get("cost", 0.0),
                    category=act.get("category", "Sightseeing"),
                    explanation=act.get("why_recommended", ""),
                    citations=[act.get("source", "Guidebook")] if act.get("source") else [],
                    risk_score=0.95,
                )
                self._db.add(activity)

            variants.append(itinerary)

        await self._db.flush()
        return variants

    async def get_active_itinerary(self, trip_id: int) -> Itinerary | None:
        """Fetch primary active itinerary containing all related activities."""
        return await self._itinerary_repo.get_active_variant(trip_id)
overrides = {}
