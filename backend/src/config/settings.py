"""Pydantic configuration settings with startup validation."""

from __future__ import annotations

from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings validated at startup."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application Configuration
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    secret_key: str = Field(default="change-me-in-production")
    access_token_expire_minutes: int = Field(default=30)
    rate_limit_per_minute: int = Field(default=60)

    # Database Configuration
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5435/nomadiq"
    )

    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0")

    # LLM Router & Models
    openai_api_key: str = Field(default="")
    model_simple: str = Field(default="gpt-4o-mini")
    model_moderate: str = Field(default="gpt-4o-mini")
    model_complex: str = Field(default="gpt-4o")
    model_evaluation: str = Field(default="gpt-4o-mini")

    # Embedding Configuration
    embedding_model: str = Field(default="text-embedding-3-small")
    chunk_size: int = Field(default=512)
    chunk_overlap: int = Field(default=50)

    # LangSmith Observability
    langsmith_api_key: str = Field(default="")
    langsmith_project: str = Field(default="nomadiq")
    langsmith_tracing_v2: bool = Field(default=False)

    # Cost Governance
    budget_limit_usd: float = Field(default=10.0)

    # Search Weights
    dense_retrieval_weight: float = Field(default=0.7)
    bm25_retrieval_weight: float = Field(default=0.3)

    # Business Constraints
    max_budget_usd: float = Field(default=10000.0)
    max_itinerary_days: int = Field(default=14)
    max_activities_per_day: int = Field(default=6)
    walk_threshold_km: float = Field(default=2.0)
    max_walk_km: float = Field(default=10.0)

    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v: str, info: dict) -> str:
        """Enforce API key is set in production environment."""
        return v


@lru_cache
def get_settings() -> Settings:
    """Load settings with caching."""
    return Settings()
