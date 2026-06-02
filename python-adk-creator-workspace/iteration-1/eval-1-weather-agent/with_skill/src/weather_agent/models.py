"""Pydantic models for weather data and responses."""

from typing import Optional, List
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Current weather data model."""
    
    location: str = Field(..., description="Location name")
    temperature: float = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition (e.g., Sunny, Cloudy)")
    humidity: int = Field(..., description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    feels_like: float = Field(..., description="Feels-like temperature in Celsius")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "San Francisco",
                "temperature": 20.5,
                "condition": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 12.5,
                "feels_like": 19.0
            }
        }


class ForecastDay(BaseModel):
    """Single day forecast model."""
    
    date: str = Field(..., description="Forecast date (YYYY-MM-DD)")
    high_temp: float = Field(..., description="High temperature in Celsius")
    low_temp: float = Field(..., description="Low temperature in Celsius")
    condition: str = Field(..., description="Weather condition")
    precipitation_chance: int = Field(..., description="Chance of precipitation (%)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15",
                "high_temp": 22.5,
                "low_temp": 15.0,
                "condition": "Sunny",
                "precipitation_chance": 10
            }
        }


class WeatherForecast(BaseModel):
    """Multi-day weather forecast model."""
    
    location: str = Field(..., description="Location name")
    forecast_days: List[ForecastDay] = Field(..., description="List of forecast days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "San Francisco",
                "forecast_days": [
                    {
                        "date": "2024-01-15",
                        "high_temp": 22.5,
                        "low_temp": 15.0,
                        "condition": "Sunny",
                        "precipitation_chance": 10
                    }
                ]
            }
        }


class AgentResponse(BaseModel):
    """Response model from the weather agent."""
    
    query: str = Field(..., description="Original user query")
    response: str = Field(..., description="Agent response")
    weather_data: Optional[WeatherData] = Field(None, description="Current weather data if applicable")
    forecast: Optional[WeatherForecast] = Field(None, description="Forecast data if applicable")
    tool_calls: List[str] = Field(default_factory=list, description="List of tools called")
