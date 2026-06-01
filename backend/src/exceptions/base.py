"""Base exception definition for all custom NomadIQ exceptions."""

from __future__ import annotations


class NomadIQError(Exception):
    """Base exception class for NomadIQ platform errors."""

    def __init__(
        self, detail: str, status_code: int = 500, error_code: str | None = None
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
