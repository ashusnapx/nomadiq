# Domain Layer

## Purpose
Specifies core shared enums, types, and architectural primitives to decouple structural definitions from application packages.

## Ownership
Product & Domain Architecture Teams

## Dependencies
- Standard library typing only to ensure maximum transportability.

## Extension Strategy
Add new enums directly to `enums.py` and structural validation types to `types.py`. Expose them via `__init__.py`.
