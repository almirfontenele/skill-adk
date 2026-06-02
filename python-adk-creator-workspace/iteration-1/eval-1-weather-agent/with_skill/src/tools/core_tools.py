"""Core weather tools for the Weather Agent."""

import json
from typing import Optional
from datetime import datetime, timedelta


def get_current_weather(location: str) -> str:
    """
    Get the current weather for a specified location.

    This tool retrieves current weather conditions including temperature,
    humidity, wind speed, and weather description for any location.

    Args:
        location: City name or location (e.g., "San Francisco, CA" or "London")

    Returns:
        str: A JSON string containing current weather information.

    Example:
        >>> get_current_weather("New York")
        '{"location": "New York", "temperature": 72, "humidity": 65, ...}'
    """
    # Simulate weather data - in production, this would call a real weather API
    # You can integrate with OpenWeatherMap, Weather API, etc.

    weather_data = {
        "location": location,
        "temperature": 72,
        "feels_like": 70,
        "humidity": 65,
        "wind_speed": 12,
        "wind_direction": "NW",
        "condition": "Partly Cloudy",
        "uv_index": 6,
        "visibility": 10,
        "pressure": 1013,
        "timestamp": datetime.now().isoformat(),
    }

    return json.dumps(weather_data)


def get_weather_forecast(location: str, days: int = 5) -> str:
    """
    Get the weather forecast for a specified location.

    This tool provides a multi-day weather forecast including temperature
    ranges, precipitation probability, and expected weather conditions.

    Args:
        location: City name or location (e.g., "San Francisco, CA")
        days: Number of days to forecast (1-10, default 5)

    Returns:
        str: A JSON string containing forecast data for the requested days.

    Example:
        >>> get_weather_forecast("London", days=3)
        '{"location": "London", "forecast": [...]}'
    """
    # Validate days parameter
    days = max(1, min(days, 10))

    # Simulate forecast data - in production, this would call a real weather API
    forecast_days = []
    base_date = datetime.now()

    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        forecast_days.append(
            {
                "date": forecast_date.strftime("%Y-%m-%d"),
                "day_of_week": forecast_date.strftime("%A"),
                "high_temp": 75 - i,
                "low_temp": 60 - i,
                "condition": ["Sunny", "Partly Cloudy", "Cloudy", "Rainy"][i % 4],
                "precipitation_chance": [10, 20, 30, 60][i % 4],
                "wind_speed": 10 + (i * 2),
                "humidity": 50 + (i * 5),
            }
        )

    forecast_data = {
        "location": location,
        "forecast": forecast_days,
        "generated_at": datetime.now().isoformat(),
    }

    return json.dumps(forecast_data)


def get_weather_alerts(location: str) -> str:
    """
    Get active weather alerts for a specified location.

    This tool retrieves any active weather alerts such as storms,
    heat warnings, or other severe weather conditions.

    Args:
        location: City name or location (e.g., "Miami, FL")

    Returns:
        str: A JSON string containing active alerts, or empty array if none.

    Example:
        >>> get_weather_alerts("Miami, FL")
        '{"location": "Miami, FL", "alerts": []}'
    """
    # Simulate alert data
    alerts_data = {
        "location": location,
        "alerts": [],
        "checked_at": datetime.now().isoformat(),
    }

    # In production, this would check a real weather alert API
    # and populate with actual warning data

    return json.dumps(alerts_data)


def format_weather_response(weather_json: str) -> str:
    """
    Format raw weather JSON data into human-readable text.

    Args:
        weather_json: JSON string from weather API

    Returns:
        str: Formatted weather description
    """
    try:
        data = json.loads(weather_json)
        location = data.get("location", "Unknown location")
        temperature = data.get("temperature", "N/A")
        condition = data.get("condition", "Unknown")
        humidity = data.get("humidity", "N/A")
        wind_speed = data.get("wind_speed", "N/A")

        return (
            f"Weather in {location}: {temperature}°F, {condition}. "
            f"Humidity: {humidity}%, Wind: {wind_speed} mph"
        )
    except json.JSONDecodeError:
        return "Unable to format weather data"
