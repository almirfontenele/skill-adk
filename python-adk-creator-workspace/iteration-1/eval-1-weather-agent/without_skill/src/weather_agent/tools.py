"""Weather tools for the Gemini agent."""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import random
from .models import WeatherData, ForecastDay, WeatherForecast


class WeatherTools:
    """Collection of weather tools for the agent."""
    
    @staticmethod
    def get_current_weather(location: str) -> Dict[str, Any]:
        """
        Get current weather for a specific location.
        
        Args:
            location: The city name or location
            
        Returns:
            Dictionary containing current weather data
        """
        # In production, this would call a real weather API (OpenWeatherMap, WeatherAPI, etc.)
        # For demonstration, we return simulated data
        
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Foggy"]
        condition = random.choice(weather_conditions)
        
        weather_data = WeatherData(
            location=location,
            temperature=round(random.uniform(10, 30), 1),
            condition=condition,
            humidity=random.randint(40, 90),
            wind_speed=round(random.uniform(0, 20), 1),
            feels_like=round(random.uniform(8, 28), 1)
        )
        
        return {
            "status": "success",
            "data": weather_data.model_dump()
        }
    
    @staticmethod
    def get_weather_forecast(location: str, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a specific location.
        
        Args:
            location: The city name or location
            days: Number of forecast days (default 5)
            
        Returns:
            Dictionary containing forecast data
        """
        # In production, this would call a real weather API
        # For demonstration, we return simulated forecast data
        
        if days > 14:
            days = 14
        if days < 1:
            days = 1
        
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Foggy"]
        forecast_days = []
        
        for i in range(days):
            forecast_date = datetime.now() + timedelta(days=i+1)
            forecast_days.append(
                ForecastDay(
                    date=forecast_date.strftime("%Y-%m-%d"),
                    high_temp=round(random.uniform(18, 28), 1),
                    low_temp=round(random.uniform(10, 20), 1),
                    condition=random.choice(weather_conditions),
                    precipitation_chance=random.randint(0, 100)
                )
            )
        
        forecast = WeatherForecast(
            location=location,
            forecast_days=forecast_days
        )
        
        return {
            "status": "success",
            "data": forecast.model_dump()
        }
    
    @staticmethod
    def compare_weather(location1: str, location2: str) -> Dict[str, Any]:
        """
        Compare current weather between two locations.
        
        Args:
            location1: First location name
            location2: Second location name
            
        Returns:
            Dictionary containing comparison data
        """
        weather1 = WeatherTools.get_current_weather(location1)
        weather2 = WeatherTools.get_current_weather(location2)
        
        return {
            "status": "success",
            "location1": weather1["data"],
            "location2": weather2["data"],
            "comparison": {
                "warmer_location": location1 if weather1["data"]["temperature"] > weather2["data"]["temperature"] else location2,
                "temperature_difference": abs(weather1["data"]["temperature"] - weather2["data"]["temperature"])
            }
        }
    
    @staticmethod
    def get_weather_alerts(location: str) -> Dict[str, Any]:
        """
        Get weather alerts for a location (if any).
        
        Args:
            location: The city name or location
            
        Returns:
            Dictionary containing alert information
        """
        # In production, this would query a real alerts API
        alerts = []
        
        # Simulated alerts (80% chance no alerts)
        if random.random() > 0.8:
            alerts.append({
                "type": "Thunderstorm Warning",
                "severity": "Moderate",
                "description": "Severe thunderstorms expected in the area"
            })
        
        return {
            "status": "success",
            "location": location,
            "alerts": alerts,
            "alert_count": len(alerts)
        }
    
    @staticmethod
    def get_all_tools() -> list:
        """
        Get all available weather tools for function calling.
        
        Returns:
            List of tool definitions for the Gemini agent
        """
        return [
            WeatherTools.get_current_weather,
            WeatherTools.get_weather_forecast,
            WeatherTools.compare_weather,
            WeatherTools.get_weather_alerts
        ]
