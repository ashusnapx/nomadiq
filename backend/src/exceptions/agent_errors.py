"""Exceptions raised during AI Agent parsing or execution workflows."""

from __future__ import annotations

from backend.src.exceptions.base import NomadIQError


class AgentExecutionError(NomadIQError):
    """Raised when an agent workflow node fails to run or complete."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=500, error_code="AGENT_EXECUTION_FAILED")


class AgentTimeoutError(NomadIQError):
    """Raised when an agent execution exceeds SLA limits."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=504, error_code="AGENT_TIMEOUT")


class PromptLoadError(NomadIQError):
    """Raised when a specified prompt template fails to load or render."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=500, error_code="PROMPT_LOAD_ERROR")
