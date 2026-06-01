"""Model router that executes LLM calls based on task complexity with fallback layers."""

from __future__ import annotations

import logging
from enum import Enum
from openai import AsyncOpenAI

from backend.src.config.settings import get_settings
from backend.src.observability.cost_tracker import cost_tracker

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    """Complexity buckets to guide LLM instance routing."""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EVALUATION = "evaluation"


class ModelRouter:
    """Intelligently matches LLM queries to optimal size/cost models with fallbacks."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._openai_key = self.settings.openai_api_key
        
        # Check if key is a Gemini API key (starts with AIzaSy)
        self._is_gemini = self._openai_key.startswith("AIzaSy") if self._openai_key else False
        
        if self._is_gemini:
            logger.info("Gemini API key detected. Configuring model router for Google Generative AI OpenAI-compatible endpoint.")
            self._client = AsyncOpenAI(
                api_key=self._openai_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            # Map all models to Gemini models
            self._models = {
                TaskComplexity.SIMPLE: "gemini-3.1-flash-lite",
                TaskComplexity.MODERATE: "gemini-3.1-flash-lite",
                TaskComplexity.COMPLEX: "gemini-3.1-flash-lite",
                TaskComplexity.EVALUATION: "gemini-3.1-flash-lite",
            }
            self._fallbacks = ["gemini-3.1-flash-lite"]
        else:
            # Lazy client loading
            self._client = (
                AsyncOpenAI(api_key=self._openai_key) if self._openai_key else None
            )
            self._models = {
                TaskComplexity.SIMPLE: self.settings.model_simple,
                TaskComplexity.MODERATE: self.settings.model_moderate,
                TaskComplexity.COMPLEX: self.settings.model_complex,
                TaskComplexity.EVALUATION: self.settings.model_evaluation,
            }
            # Fallback hierarchy
            self._fallbacks = [
                self.settings.model_complex,
                self.settings.model_moderate,
                self.settings.model_simple,
            ]

    async def invoke(
        self,
        messages: list[dict],
        complexity: TaskComplexity,
        temperature: float | None = None,
        response_format: dict | None = None,
    ) -> dict:
        """Execute LLM call by routing to configured model with failure safety."""
        model = self._models.get(complexity, self.settings.model_simple)
        temp = temperature if temperature is not None else 0.7

        # Gemini compatibility: ensure at least one user message is present
        has_user = any(m.get("role") == "user" for m in messages)
        if not has_user:
            messages.append({"role": "user", "content": "Generate the structured plan based on the system instructions."})

        # Dynamic local mock fallback if API key is absent
        if not self._client:
            logger.warning(
                f"No OpenAI key detected. Mocking response for model: {model}"
            )
            return self._mock_response(model, messages)

        try:
            return await self._call_api(model, messages, temp, response_format)
        except Exception as exc:
            logger.error(
                f"Primary model {model} failed: {exc}. Commencing fallback routine."
            )
            return await self._execute_fallback(messages, temp, response_format, exclude=model)

    async def _call_api(
        self, model: str, messages: list[dict], temp: float, resp_fmt: dict | None
    ) -> dict:
        kwargs: dict = {
            "model": model,
            "messages": messages,
            "temperature": temp,
        }
        if resp_fmt:
            kwargs["response_format"] = resp_fmt

        resp = await self._client.chat.completions.create(**kwargs)
        usage = resp.usage
        prompt_t = usage.prompt_tokens if usage else 0
        comp_t = usage.completion_tokens if usage else 0

        # Record metrics in cost tracker
        cost_tracker.record(model, prompt_t, comp_t)

        return {
            "content": resp.choices[0].message.content or "{}",
            "model": model,
            "usage": {"prompt_tokens": prompt_t, "completion_tokens": comp_t},
        }

    async def _execute_fallback(
        self,
        messages: list[dict],
        temp: float,
        resp_fmt: dict | None,
        exclude: str,
    ) -> dict:
        for model in self._fallbacks:
            if model == exclude:
                continue
            try:
                logger.info(f"Attempting fallback model: {model}")
                return await self._call_api(model, messages, temp, resp_fmt)
            except Exception as exc:
                logger.error(f"Fallback model {model} failed: {exc}")
                continue

        # Fail-safe final mock option to prevent platform crash
        logger.critical("All model routing options exhausted. Issuing mock fallback.")
        return self._mock_response(exclude, messages)

    def _mock_response(self, model: str, messages: list[dict]) -> dict:
        """Produce deterministic mock responses to enable offline operation."""
        # Simple parser for mock structures
        prompt_text = "".join([m.get("content", "") for m in messages]).lower()
        content = "{}"
        if "user_preference" in prompt_text or "preference" in prompt_text:
            content = json.dumps({
                "interests": ["Sightseeing", "Food"],
                "dietary": [],
                "mobility": "Standard",
                "pace": "moderate",
                "accommodation": "mid-range",
                "must_see": ["Central Park"],
                "avoid_list": []
            })
        elif "destination_research" in prompt_text or "research" in prompt_text:
            content = json.dumps([{
                "name": "Central Park Walk",
                "category": "Sightseeing",
                "cost": 0.0,
                "duration": 2.0,
                "best_time": "Morning",
                "location": "Manhattan",
                "why_recommended": "Matches Sightseeing preference",
                "confidence": 0.95,
                "source": "Retrieved Guidebook"
            }])
        elif "weather_intelligence" in prompt_text or "weather" in prompt_text:
            content = json.dumps({
                "daily_weather": [{"day": 1, "condition": "Sunny", "temp": 22}],
                "activity_impacts": [{"activity_id": 1, "suitability": 1.0}],
                "disruption_risks": [],
                "weather_score": 0.9
            })
        elif "transportation" in prompt_text or "transit" in prompt_text:
            content = json.dumps({
                "route_segments": [{"from": "Hotel", "to": "Central Park", "mode": "Walking", "duration": 15, "cost": 0.0}],
                "total_cost": 0.0,
                "total_time": 15
            })
        elif "optimization" in prompt_text or "optimize" in prompt_text:
            content = json.dumps({
                "Plan A (Balanced)": {"activities": [], "cost": 150.0, "confidence": 0.9},
                "Plan B (Budget-Focused)": {"activities": [], "cost": 80.0, "confidence": 0.8},
                "Plan C (Experience-Focused)": {"activities": [], "cost": 300.0, "confidence": 0.95}
            })
        elif "safety" in prompt_text or "safe" in prompt_text:
            content = json.dumps({
                "safety_score": 1.0,
                "assessments": [],
                "warnings": [],
                "emergency_info": "Call 911"
            })
        elif "replan" in prompt_text:
            content = json.dumps({
                "modified_activities": [],
                "preserved_activities": [],
                "cost_delta": 0.0,
                "explanation": "Weather disruption resolved successfully."
            })
        else:
            content = json.dumps({"itinerary": "Mocked generic response content."})

        return {
            "content": content,
            "model": f"{model}-mock",
            "usage": {"prompt_tokens": 100, "completion_tokens": 100},
        }


import json
overrides = {}
