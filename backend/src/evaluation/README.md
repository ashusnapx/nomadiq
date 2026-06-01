# Evaluation Framework

## Purpose
Supports automated scoring of itinerary generation output quality (relevance, budget utilization, time boundaries, hallucination rate) against traveler constraints.

## Ownership
Engineering Platform & AI Team

## Structure
- `evaluation_engine.py`: Evaluator utilizing LLM judges.

## Extension Strategy
Add specialized evaluation rules (e.g., semantic grounding similarity comparisons) directly in `evaluation_engine.py` or compile new prompt versions under templates.
