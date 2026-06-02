"""Weather Agent - A production-ready weather agent using Gemini API."""

__version__ = "1.0.0"
__author__ = "Weather Agent Team"

from .agent import WeatherAgent
from .tools import WeatherTools

__all__ = ["WeatherAgent", "WeatherTools"]
