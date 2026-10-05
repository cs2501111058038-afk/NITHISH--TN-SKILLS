from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase API"
    app_version: str = "1.0.0"
    environment: str = "development"

    gemini_api_key: str = ""

    # Keep the model configurable because Gemini model availability changes.
    gemini_model: str = "gemini-3.8-flash"

    # Useful for testing the complete application without an API key.
    mock_ai: bool = False

    cors_origins: str = "http://localhost:8501"

    max_terms: int = 30
    max_input_chars: int = 20000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()