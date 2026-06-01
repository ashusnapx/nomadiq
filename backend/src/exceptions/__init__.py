"""Exceptions package grouping platform errors and exception handlers."""

from __future__ import annotations

from backend.src.exceptions.base import NomadIQError
from backend.src.exceptions.handlers import register_exception_handlers

__all__ = ["NomadIQError", "register_exception_handlers"]
