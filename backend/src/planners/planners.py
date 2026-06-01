"""Itinerary Planners and sequence ordering utilities."""

from __future__ import annotations


class SimplePlanner:
    """Arranges activities into optimal chronological slots (Morning, Afternoon, Evening)."""

    def sequence_day(self, activities: list[dict]) -> list[dict]:
        """Sequence activities based on time_slot preferences."""
        order = {"Morning": 0, "Lunch": 1, "Afternoon": 2, "Dinner": 3, "Evening": 4}

        def get_order(act: dict) -> int:
            return order.get(act.get("time_slot", "Afternoon"), 2)

        return sorted(activities, key=get_order)
overrides = {}
