# Prompts

## Purpose
External prompt templates for all NomadIQ agents. Prompts are never embedded in source code.

## Ownership
AI/ML Engineering Team

## Structure
```
templates/
├── system/v1/        # Agent system prompts
├── planner/v1/       # Planning and summary prompts
├── research/v1/      # Research and query generation
├── replanning/v1/    # Dynamic replanning prompts
├── safety/v1/        # Safety review prompts
└── evaluation/v1/    # Quality evaluation prompts
```

## Dependencies
- `registry.py` loads and caches templates
- `loader.py` provides convenience functions per category

## Extension Strategy
1. Create a new version directory (e.g., `v2/`) alongside existing versions
2. Register new prompts in the same category structure
3. Update agent code to reference the new version
4. Old versions remain available for rollback and A/B testing

## Versioning
Each prompt is versioned by directory. The registry tracks content hashes for change detection.
