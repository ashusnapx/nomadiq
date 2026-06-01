# Integrations Layer

## Purpose
Manages connections to AI providers via the Model Router, dynamic third-party plugins, and synthetic data modules.

## Ownership
Engineering Platform Team

## Structure
- `model_router.py`: Handles model orchestration, fallback chains, and offline mocks.
- `plugin_system.py`: The interface definition for external providers.
- `providers/`: Concrete default plugins for weather, transit routing, and mapping coordinates.

## Extension Strategy
Implement abstract classes defined in `plugin_system.py` (e.g., `WeatherProvider`) and register new plugins with the global `plugin_registry`.
