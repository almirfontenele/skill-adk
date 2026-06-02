"""Configuration management for the Weather Agent."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for Weather Agent."""
    
    # Google Generative AI Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Weather API Configuration (optional, for enhanced data)
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")
    
    # Agent Configuration
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please configure it in your .env file."
            )
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """Get configuration as dictionary."""
        return {
            "google_api_key": cls.GOOGLE_API_KEY,
            "gemini_model": cls.GEMINI_MODEL,
            "weather_api_key": cls.WEATHER_API_KEY,
            "max_retries": cls.MAX_RETRIES,
            "timeout": cls.TIMEOUT,
        }
