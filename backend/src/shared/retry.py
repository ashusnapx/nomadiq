"""Retry utility implementing exponential backoff with random jitter."""

from __future__ import annotations

import asyncio
import random
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar, ParamSpec

logger = logging.getLogger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay_sec: float = 1.0,
    max_delay_sec: float = 8.0,
    retry_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[
    [Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, T]]
]:
    """Decorator retrying async calls with exponential backoff and jitter."""

    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            retries = 0
            delay = base_delay_sec

            while True:
                try:
                    return await func(*args, **kwargs)
                except retry_exceptions as exc:
                    retries += 1
                    if retries > max_retries:
                        logger.error(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}."
                        )
                        raise exc

                    # Calculate exponential delay with full jitter
                    jittered_delay = random.uniform(0.5 * delay, 1.5 * delay)
                    jittered_delay = min(jittered_delay, max_delay_sec)

                    logger.warning(
                        f"Attempt {retries} failed for {func.__name__}: {exc}. "
                        f"Retrying in {jittered_delay:.2f} seconds..."
                    )
                    await asyncio.sleep(jittered_delay)

                    delay *= 2

        return wrapper

    return decorator
overrides = {}
