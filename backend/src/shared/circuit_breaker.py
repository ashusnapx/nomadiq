"""Circuit Breaker resilience pattern implementation for protecting external calls."""

from __future__ import annotations

import time
import logging
from enum import Enum
from typing import Any, Callable, Coroutine, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Available circuit states."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """Protects external systems from cascade failures using a state machine."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_state_change = time.time()

    async def call(
        self, func: Callable[..., Coroutine[Any, Any, T]], *args: Any, **kwargs: Any
    ) -> T:
        """Call target coroutine under circuit breaker constraints."""
        current_time = time.time()

        # Handle Transition from OPEN to HALF-OPEN
        if self.state == CircuitState.OPEN:
            if current_time - self.last_state_change > self.recovery_timeout_sec:
                self._transition_to(CircuitState.HALF_OPEN)
            else:
                raise RuntimeError(
                    f"Circuit breaker '{self.name}' is OPEN. Request blocked."
                )

        try:
            result = await func(*args, **kwargs)
            # If we succeed in HALF-OPEN, close the circuit
            if self.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.CLOSED)
            return result
        except Exception as exc:
            self._handle_failure()
            raise exc

    def _transition_to(self, new_state: CircuitState) -> None:
        logger.warning(
            f"Circuit '{self.name}' transitioning: {self.state.value} -> {new_state.value}"
        )
        self.state = new_state
        self.last_state_change = time.time()
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0

    def _handle_failure(self) -> None:
        self.failure_count += 1
        logger.error(
            f"Circuit '{self.name}' failure recorded. Count: {self.failure_count}/{self.failure_threshold}"
        )
        if self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
            if self.failure_count >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
overrides = {}
