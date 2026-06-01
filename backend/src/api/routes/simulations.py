"""Simulations API Router exposing What-If simulation parameters."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.shared.database import get_db
from backend.src.schemas.whatif import WhatIfRequest, WhatIfResponse
from backend.src.services.whatif_service import WhatIfService

router = APIRouter(prefix="/simulations", tags=["Simulations"])


@router.post("", response_model=WhatIfResponse, status_code=200)
async def simulate_whatif(
    payload: WhatIfRequest, db: AsyncSession = Depends(get_db)
) -> WhatIfResponse:
    """Simulate hypothetical budget cuts or weather conditions and return comparison metrics."""
    service = WhatIfService(db)
    res = await service.simulate_scenario(
        trip_id=payload.trip_id,
        scenario_type=payload.scenario_type,
        parameter_value=payload.parameter_value,
    )

    import datetime
    return WhatIfResponse(
        trip_id=res["trip_id"],
        scenario_description=res["scenario"],
        impact_assessment="Simulation completed successfully. Visualizing impacts on variants A/B/C.",
        results=res["results"],
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )
overrides = {}
