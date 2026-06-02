"""Pydantic models for type-safe weather data."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WeatherCondition(BaseModel):
    """Model for current weather conditions."""

    location: str
    temperature: float = Field(description="Temperature in Fahrenheit")
    feels_like: Optional[float] = None
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in mph")
    wind_direction: str
    condition: str
    uv_index: int
    visibility: float = Field(description="Visibility in miles")
    pressure: int = Field(description="Pressure in mb")
    timestamp: datetime


class ForecastDay(BaseModel):
    """Model for a single day forecast."""

    date: str
    day_of_week: str
    high_temp: float
    low_temp: float
    condition: str
    precipitation_chance: int = Field(ge=0, le=100)
    wind_speed: float
    humidity: int


class WeatherForecast(BaseModel):
    """Model for multi-day weather forecast."""

    location: str
    forecast: List[ForecastDay]
    generated_at: datetime


class WeatherAlert(BaseModel):
    """Model for weather alerts."""

    location: str
    alert_type: str
    severity: str
    description: str
    effective_from: datetime
    effective_to: Optional[datetime] = None


class WeatherAlertsResponse(BaseModel):
    """Model for weather alerts response."""

    location: str
    alerts: List[WeatherAlert] = []
    checked_at: datetime
