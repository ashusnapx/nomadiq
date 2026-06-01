"""Core Domain Enumerations for NomadIQ entities."""

from __future__ import annotations

from enum import Enum


class TripStatus(str, Enum):
    """Lifecycle status of a planned trip."""

    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ActivityType(str, Enum):
    """Categorized activity categories for recommendation engines."""

    SIGHTSEEING = "Sightseeing"
    FOOD = "Food"
    CULTURE = "Culture"
    ADVENTURE = "Adventure"
    RELAXATION = "Relaxation"
    SHOPPING = "Shopping"
    NIGHTLIFE = "Nightlife"
    NATURE = "Nature"


class TravelerPersona(str, Enum):
    """Traveler archetype to dictate default behaviors."""

    ADVENTURE_SEEKER = "Adventure Seeker"
    LUXURY_TRAVELER = "Luxury Traveler"
    FOOD_EXPLORER = "Food Explorer"
    NATURE_ENTHUSIAST = "Nature Enthusiast"
    BALANCED = "Balanced Traveler"


class EventType(str, Enum):
    """Real-time event disruption types."""

    RAIN = "Rain"
    STORM = "Storm"
    FLIGHT_DELAY = "Flight Delay"
    TRAIN_DELAY = "Train Delay"
    ATTRACTION_CLOSURE = "Attraction Closure"
    TRAFFIC_CONGESTION = "Traffic Congestion"
    BUDGET_OVERRUN = "Budget Overrun"


class RiskLevel(str, Enum):
    """Travel safety risk assessment levels."""

    SAFE = "Safe"
    CAUTION = "Caution"
    WARNING = "Warning"
    DANGER = "Danger"


class WeatherCondition(str, Enum):
    """Standardized daily weather forecasts."""

    SUNNY = "Sunny"
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    STORMY = "Stormy"
    SNOWY = "Snowy"


class TransportMode(str, Enum):
    """Supported transit modes."""

    WALKING = "Walking"
    PUBLIC_TRANSIT = "Public Transit"
    TAXI = "Taxi/Rideshare"
    RENTAL_CAR = "Rental Car"


class PlanVariant(str, Enum):
    """Variants of optimization plans."""

    A = "Plan A (Balanced)"
    B = "Plan B (Budget-Focused)"
    C = "Plan C (Experience-Focused)"
