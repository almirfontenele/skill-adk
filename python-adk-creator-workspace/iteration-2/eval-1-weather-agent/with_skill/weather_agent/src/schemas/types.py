"""Pydantic models for structured data used across the project."""

from pydantic import BaseModel


class WeatherData(BaseModel):
    """Current weather conditions for a city."""

    city: str
    temperature_celsius: float
    condition: str
    humidity_percent: int
    wind_speed_kmh: float


class ForecastDay(BaseModel):
    """Weather forecast for a single day."""

    date: str
    high_celsius: float
    low_celsius: float
    condition: str


class WeatherForecast(BaseModel):
    """Multi-day weather forecast for a city."""

    city: str
    forecast_days: int
    forecast: list[ForecastDay]
