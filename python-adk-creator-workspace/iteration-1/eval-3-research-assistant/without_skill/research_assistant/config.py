"""Configuration management for the research assistant."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


class Config:
    """Base configuration."""

    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    MODEL = os.getenv("MODEL", "gemini-2.5-flash")

    # Search Configuration
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "10"))

    # Summarization Configuration
    SUMMARIZATION_LENGTH = int(os.getenv("SUMMARIZATION_LENGTH", "500"))
    MIN_SUMMARY_LENGTH = 100

    # Agent Configuration
    TEMPERATURE = 0.7
    TOP_P = 0.9
    MAX_TOKENS = 2048

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is set."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        return True


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TEMPERATURE = 0.9


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TEMPERATURE = 0.5


def get_config(env: str = "development") -> Config:
    """Get configuration based on environment."""
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }
    return configs.get(env, DevelopmentConfig)
