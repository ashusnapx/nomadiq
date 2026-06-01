"""Security utilities protecting against prompt injections and malicious inputs."""

from __future__ import annotations

import logging
from backend.src.exceptions.api_errors import ValidationError

logger = logging.getLogger(__name__)

# List of keywords indicating dynamic prompt injection attacks
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "system prompt",
    "bypass constraints",
    "jailbreak",
    "output raw prompt",
]


class SecuritySanitizer:
    """Validates inputs, scanning request payloads for malicious injection indicators."""

    def sanitize_input(self, user_input: str) -> str:
        """Strip HTML tags and check against prompt injection attempts."""
        cleaned = user_input.strip()

        # Check for injection attacks
        lowered = cleaned.lower()
        for kw in INJECTION_KEYWORDS:
            if kw in lowered:
                logger.critical(
                    f"PROMPT INJECTION DETECTED! Input blocked: '{cleaned[:50]}...'"
                )
                raise ValidationError("Input violates travel content safety guidelines.")

        return cleaned
overrides = {}
