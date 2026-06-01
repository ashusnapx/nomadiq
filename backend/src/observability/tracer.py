"""OpenTelemetry-style logging tracers to monitor system latency."""

from __future__ import annotations

import time
import logging
from typing import Any, Callable, Coroutine, TypeVar, ParamSpec

logger = logging.getLogger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


class ObservabilityTracer:
    """Manages spans, measures workflow execution durations, and records token usage costs."""

    def __init__(self) -> None:
        self._spans: list[dict] = []

    def record_span(self, name: str, duration_ms: float, metadata: dict) -> None:
        """Log transaction span with metadata."""
        span = {
            "name": name,
            "duration_ms": duration_ms,
            "metadata": metadata,
            "timestamp": time.time(),
        }
        self._spans.append(span)
        logger.info(f"Span recorded: {name} (Duration: {duration_ms:.2f}ms)")

    def get_traces(self) -> list[dict]:
        """Fetch all recorded spans."""
        return list(self._spans)


tracer = ObservabilityTracer()


def observed_span(span_name: str) -> Callable[
    [Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, T]]
]:
    """Decorator to measure and trace asynchronous methods."""

    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            start = time.perf_counter()
            try:
                res = await func(*args, **kwargs)
                return res
            finally:
                dur = (time.perf_counter() - start) * 1000
                tracer.record_span(span_name, dur, {"function": func.__name__})

        return wrapper

    return decorator
overrides = {}
