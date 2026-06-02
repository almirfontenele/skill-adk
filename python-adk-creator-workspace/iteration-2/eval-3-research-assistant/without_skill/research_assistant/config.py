"""Configuration for the Research Assistant."""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # Google GenAI / Gemini
    gemini_api_key: str = field(default_factory=lambda: os.environ.get("GEMINI_API_KEY", ""))
    gemini_model: str = field(default_factory=lambda: os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"))

    # Web search (SerpAPI — free tier available at serpapi.com)
    serpapi_key: str = field(default_factory=lambda: os.environ.get("SERPAPI_KEY", ""))

    # Behaviour
    max_search_results: int = field(
        default_factory=lambda: int(os.environ.get("MAX_SEARCH_RESULTS", "5"))
    )
    summary_max_words: int = field(
        default_factory=lambda: int(os.environ.get("SUMMARY_MAX_WORDS", "300"))
    )

    def validate(self) -> None:
        """Raise ValueError if required settings are missing."""
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Get your key at https://aistudio.google.com/app/apikey"
            )
