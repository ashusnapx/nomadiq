# Observability Layer

## Purpose
Enables comprehensive monitoring: captures request spans, logs LLM token usage, calculates expenditures, and integrates OpenTelemetry.

## Ownership
Engineering Platform Team

## Structure
- `cost_tracker.py`: Tracks token expenditures.
- `tracer.py`: Measures latencies across agent workflows.

## Extension Strategy
Add OpenTelemetry collector metrics reporting inside `tracer.py`. Ensure tracers are lightweight and do not impact page loads.
