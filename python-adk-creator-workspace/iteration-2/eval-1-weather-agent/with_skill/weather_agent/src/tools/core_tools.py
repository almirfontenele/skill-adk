"""Weather tools for the weather agent.

These are stub implementations. Replace with real API calls (e.g., OpenWeatherMap)
by setting WEATHER_API_KEY in .env and updating the functions below.
"""

import json
from datetime import datetime, timedelta


def get_current_weather(city: str) -> str:
    """
    Get the current weather conditions for a given city.

    Args:
        city: Name of the city to get weather for (e.g., 'São Paulo', 'London').

    Returns:
        A JSON string with current weather data including temperature, condition,
        humidity, and wind speed.
    """
    # Stub implementation — replace with a real weather API call
    data = {
        "city": city,
        "temperature_celsius": 22,
        "condition": "Partly Cloudy",
        "humidity_percent": 65,
        "wind_speed_kmh": 15,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return json.dumps(data)


def get_weather_forecast(city: str, days: int) -> str:
    """
    Get the weather forecast for a given city for the next N days.

    Args:
        city: Name of the city to get the forecast for (e.g., 'Tokyo', 'New York').
        days: Number of days to forecast (1 to 7).

    Returns:
        A JSON string with a list of daily forecast entries, each containing date,
        high/low temperature, and expected condition.
    """
    if days < 1:
        days = 1
    if days > 7:
        days = 7

    # Stub implementation — replace with a real weather API call
    forecast = []
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Thunderstorm"]
    for i in range(days):
        date = (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d")
        forecast.append({
            "date": date,
            "high_celsius": 25 - i,
            "low_celsius": 15 - i,
            "condition": conditions[i % len(conditions)],
        })

    data = {"city": city, "forecast_days": days, "forecast": forecast}
    return json.dumps(data)
