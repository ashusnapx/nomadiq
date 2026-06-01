"""FastAPI exception handlers standardizing JSON error response structures."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.src.exceptions.base import NomadIQError


def register_exception_handlers(app: FastAPI) -> None:
    """Register application-wide exception handling middleware."""

    @app.exception_handler(NomadIQError)
    async def nomadiq_error_handler(request: Request, exc: NomadIQError) -> JSONResponse:
        """Handle custom platform errors gracefully."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                },
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected runtime exceptions to avoid leaking internals."""
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred on the server.",
                },
            },
        )
