# AI Workflows Layer

## Purpose
Orchestrates AI agents into observable StateGraph state machines using LangGraph, including itinerary compilation, active replanning, and What-If simulations.

## Ownership
AI/ML Engineering Team

## Structure
- `itinerary_workflow.py`: Sequence compiler building trips (Preference -> Summary).
- `replanning_workflow.py`: Selectively recalculates slots on active delays/closures.
- `simulation_workflow.py`: Hypothetical scenario simulation.

## Extension Strategy
Add new steps, conditional edges, or state fields to individual workflow classes. Use standard LangGraph constructs. Keep files ≤100-150 lines.
