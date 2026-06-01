"""Trips API Router supporting creation, listing, and updates."""

from __future__ import annotations

from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.shared.database import get_db
from backend.src.schemas.trip import TripCreate, TripUpdate, TripResponse
from backend.src.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(
    payload: TripCreate, db: AsyncSession = Depends(get_db)
) -> TripResponse:
    """Create a new Trip resource with initial constraints."""
    service = TripService(db)
    return await service.create_trip(payload)


@router.get("", response_model=list[TripResponse])
async def list_trips(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> Sequence[TripResponse]:
    """Retrieve all trips using offset pagination boundaries."""
    service = TripService(db)
    return await service.list_trips(skip, limit)


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: int, db: AsyncSession = Depends(get_db)
) -> TripResponse:
    """Fetch details of a single Trip by primary key."""
    service = TripService(db)
    return await service.get_trip(trip_id)


@router.patch("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: int, payload: TripUpdate, db: AsyncSession = Depends(get_db)
) -> TripResponse:
    """Modify preferences or lifecycle state of an existing Trip."""
    service = TripService(db)
    return await service.update_trip(trip_id, payload)
