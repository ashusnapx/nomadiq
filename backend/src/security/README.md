# Security Layer

## Purpose
Exposes sanitizers mapping and blocking prompt injection keywords, ensuring safety before queries reach model boundaries.

## Ownership
Engineering Security & Platform Teams

## Structure
- `sanitizer.py`: Strip tools and prompt injection block lists.

## Extension Strategy
Add new injection keywords or regular expressions to block sophisticated evasion prompts inside `sanitizer.py`. Keep scans rapid and efficient.
```
