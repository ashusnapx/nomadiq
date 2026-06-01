"""Memory utilities for handling ephemeral session buffers."""

from __future__ import annotations


class ConversationMemory:
    """Holds active memory blocks in memory, providing rolling summaries."""

    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self._buffer: list[dict] = []

    def add_turn(self, role: str, text: str) -> None:
        """Append conversational turn to the memory window."""
        self._buffer.append({"role": role, "content": text})
        if len(self._buffer) > self.window_size:
            self._buffer.pop(0)

    def get_messages(self) -> list[dict]:
        """Fetch all messages within the active rolling window."""
        return list(self._buffer)

    def clear(self) -> None:
        """Clear active memory cache."""
        self._buffer.clear()
overrides = {}
