# Configuration Layer

## Purpose
Manages env-based parameters, feature flags, and business constants for the NomadIQ application.

## Ownership
Engineering Platform Team

## Dependencies
- `pydantic-settings` for environment validation.
- Internal settings are loaded on startup and cached.

## Extension Strategy
- **Settings**: Add variables as fields to the `Settings` class in `settings.py` with appropriate types and default values.
- **Feature Flags**: Add new flag keys to the default dictionary in `feature_flags.py` to expose toggles.
- **Constants**: Place rigid business boundaries in `constants.py`.
