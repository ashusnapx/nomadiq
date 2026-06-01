# Notifications Layer

## Purpose
Enables fully decoupled reactive, event-driven travel updates, replanning triggers, and dead letter fallback queue operations.

## Ownership
Engineering Platform Team

## Structure
- `events.py`: Typed event definitions.
- `event_bus.py`: Core Pub/Sub message broker supporting replays and DLQ storage.

## Extension Strategy
Add new event subclasses in `events.py` and register target listeners using `event_bus.subscribe()`. Keep handlers async and non-blocking.
