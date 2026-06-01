"""AI Cost Governance tracking token expenditures and budget limits."""

from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Model unit costs per 1,000,000 tokens (Input, Output)
MODEL_PRICING = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "text-embedding-3-small": (0.02, 0.00),
    "gpt-4o-mock": (0.00, 0.00),
    "gpt-4o-mini-mock": (0.00, 0.00),
}


class CostTracker:
    """Tracks token usages, estimates request fees, and triggers budget alerts."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: list[dict] = []
        self.budget_limit_usd = 50.0

    def record(self, model: str, prompt_tokens: int, completion_tokens: int) -> dict:
        """Record token consumption event and compute cost."""
        pricing = MODEL_PRICING.get(model, (1.00, 3.00))  # Default fallback cost
        cost = (
            (prompt_tokens * pricing[0]) + (completion_tokens * pricing[1])
        ) / 1_000_000

        record = {
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": cost,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        with self._lock:
            self._records.append(record)

        total = self.total_cost_usd
        if total > self.budget_limit_usd:
            logger.critical(
                f"BUDGET EXCEEDED! Active cost: ${total:.4f} exceeds limit: ${self.budget_limit_usd:.4f}"
            )

        return record

    @property
    def total_cost_usd(self) -> float:
        """Sum of all records' calculated USD costs."""
        with self._lock:
            return sum(r["cost_usd"] for r in self._records)

    def get_summary(self) -> dict:
        """Export comprehensive token and cost breakdown dashboard metrics."""
        with self._lock:
            total_prompt = sum(r["prompt_tokens"] for r in self._records)
            total_completion = sum(r["completion_tokens"] for r in self._records)
            cost_by_model: dict[str, float] = {}
            for r in self._records:
                m = r["model"]
                cost_by_model[m] = cost_by_model.get(m, 0.0) + r["cost_usd"]

        return {
            "total_cost_usd": self.total_cost_usd,
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "cost_by_model": cost_by_model,
            "over_budget": self.total_cost_usd > self.budget_limit_usd,
            "request_count": len(self._records),
        }

    def clear(self) -> None:
        """Reset internal accumulator tracking metrics."""
        with self._lock:
            self._records.clear()


cost_tracker = CostTracker()
