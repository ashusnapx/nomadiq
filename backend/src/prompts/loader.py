"""Convenience functions for prompt loading."""

from __future__ import annotations

from backend.src.prompts.registry import prompt_registry


def load_system_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load a system-category prompt."""
    return prompt_registry.render("system", name, version, **kwargs)


def load_planner_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load a planner-category prompt."""
    return prompt_registry.render("planner", name, version, **kwargs)


def load_research_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load a research-category prompt."""
    return prompt_registry.render("research", name, version, **kwargs)


def load_replanning_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load a replanning-category prompt."""
    return prompt_registry.render("replanning", name, version, **kwargs)


def load_safety_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load a safety-category prompt."""
    return prompt_registry.render("safety", name, version, **kwargs)


def load_evaluation_prompt(name: str, version: str = "v1", **kwargs: str) -> str:
    """Load an evaluation-category prompt."""
    return prompt_registry.render("evaluation", name, version, **kwargs)
