# AI Agents Layer

## Purpose
Collects independent specialist agent entities coordinating to execute trip builders and adaptive events processing.

## Ownership
AI/ML Engineering Team

## Structure
- `base.py`: General abstract agent mechanics with prompt loaders and model routers.
- `registry.py`: Central registration database matching agent names to specs.
- Specialist agents: `user_preference`, `destination_research`, `weather_intelligence`, `transportation`, `optimization`, `safety`, `replanning`, `summary`.

## Extension Strategy
Inherit from `BaseAgent` in `base.py`, register a unique default `name`, specify its parameters, and register it via `agent_registry.register()`. Keep files ≤100 lines.
