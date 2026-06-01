"""Budget Service supplying optimizations and categorization breakdowns."""

from __future__ import annotations

from backend.src.models.itinerary import Itinerary


class BudgetService:
    """Computes total cost metrics and slices itineraries into category budget portions."""

    def calculate_breakdown(self, itinerary: Itinerary) -> dict[str, float]:
        """Group and sum activity expenditures by category."""
        breakdown: dict[str, float] = {}
        for act in itinerary.activities:
            cat = act.category
            breakdown[cat] = breakdown.get(cat, 0.0) + act.cost
        return breakdown

    def optimize_costs(self, itinerary: Itinerary, max_budget: float) -> list[dict]:
        """Identify premium activities and suggest lower cost alternatives to respect limits."""
        recommendations = []
        for act in itinerary.activities:
            if act.cost > 100.0:
                cheaper_cost = act.cost * 0.5
                recommendations.append(
                    {
                        "activity_id": act.id,
                        "name": act.name,
                        "current_cost": act.cost,
                        "suggested_cheaper_alternative": f"Standard {act.name}",
                        "estimated_saving": act.cost - cheaper_cost,
                    }
                )
        return recommendations
overrides = {}
