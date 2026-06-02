"""Weather tools for the Gemini agent using Open-Meteo (free, no API key required)."""

import httpx
from typing import Optional


def _geocode(location: str) -> tuple[float, float, str]:
    """Resolve a location name to latitude/longitude using the Open-Meteo geocoding API.

    Args:
        location: City name or location string.

    Returns:
        Tuple of (latitude, longitude, resolved_name).

    Raises:
        ValueError: If the location cannot be resolved.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}
    response = httpx.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not results:
        raise ValueError(f"Location '{location}' not found.")
    result = results[0]
    resolved = f"{result['name']}, {result.get('admin1', '')}, {result.get('country', '')}".strip(", ")
    return result["latitude"], result["longitude"], resolved


def get_current_weather(location: str) -> str:
    """Get the current weather conditions for a given location.

    Args:
        location: The city and optional state/country, e.g. 'London, UK' or 'New York, NY'.

    Returns:
        A human-readable string describing the current weather conditions.
    """
    try:
        lat, lon, resolved_name = _geocode(location)
    except (ValueError, httpx.HTTPError) as exc:
        return f"Error resolving location '{location}': {exc}"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation",
            "is_day",
        ],
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "timezone": "auto",
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        return f"Error fetching weather data: {exc}"

    current = data.get("current", {})
    units = data.get("current_units", {})

    temp = current.get("temperature_2m", "N/A")
    feels_like = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind_speed = current.get("wind_speed_10m", "N/A")
    wind_dir = current.get("wind_direction_10m", "N/A")
    precipitation = current.get("precipitation", "N/A")
    weather_code = current.get("weather_code", 0)
    condition = _wmo_description(weather_code)

    return (
        f"Current weather in {resolved_name}:\n"
        f"  Condition: {condition}\n"
        f"  Temperature: {temp}{units.get('temperature_2m', '°C')}\n"
        f"  Feels like: {feels_like}{units.get('apparent_temperature', '°C')}\n"
        f"  Humidity: {humidity}{units.get('relative_humidity_2m', '%')}\n"
        f"  Wind: {wind_speed} {units.get('wind_speed_10m', 'km/h')} from {wind_dir}°\n"
        f"  Precipitation: {precipitation} {units.get('precipitation', 'mm')}"
    )


def get_weather_forecast(location: str, days: Optional[int] = 7) -> str:
    """Get a multi-day weather forecast for a given location.

    Args:
        location: The city and optional state/country, e.g. 'Tokyo, Japan' or 'Paris'.
        days: Number of forecast days (1–16). Defaults to 7.

    Returns:
        A human-readable string with the daily weather forecast.
    """
    if days is None:
        days = 7
    days = max(1, min(days, 16))

    try:
        lat, lon, resolved_name = _geocode(location)
    except (ValueError, httpx.HTTPError) as exc:
        return f"Error resolving location '{location}': {exc}"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "sunrise",
            "sunset",
        ],
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "timezone": "auto",
        "forecast_days": days,
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        return f"Error fetching forecast data: {exc}"

    daily = data.get("daily", {})
    units = data.get("daily_units", {})
    dates = daily.get("time", [])
    codes = daily.get("weather_code", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("wind_speed_10m_max", [])
    sunrises = daily.get("sunrise", [])
    sunsets = daily.get("sunset", [])

    temp_unit = units.get("temperature_2m_max", "°C")
    precip_unit = units.get("precipitation_sum", "mm")
    wind_unit = units.get("wind_speed_10m_max", "km/h")

    lines = [f"{days}-day forecast for {resolved_name}:\n"]
    for i, date in enumerate(dates):
        condition = _wmo_description(codes[i] if i < len(codes) else 0)
        t_max = max_temps[i] if i < len(max_temps) else "N/A"
        t_min = min_temps[i] if i < len(min_temps) else "N/A"
        p = precip[i] if i < len(precip) else "N/A"
        w = wind[i] if i < len(wind) else "N/A"
        sunrise = sunrises[i].split("T")[-1] if i < len(sunrises) else "N/A"
        sunset = sunsets[i].split("T")[-1] if i < len(sunsets) else "N/A"

        lines.append(
            f"  {date}: {condition}\n"
            f"    High: {t_max}{temp_unit}, Low: {t_min}{temp_unit}\n"
            f"    Precipitation: {p} {precip_unit}, Max Wind: {w} {wind_unit}\n"
            f"    Sunrise: {sunrise}, Sunset: {sunset}"
        )

    return "\n".join(lines)


def _wmo_description(code: int) -> str:
    """Convert a WMO weather interpretation code to a human-readable description."""
    wmo_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Icy fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Heavy freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return wmo_codes.get(code, f"Unknown condition (code {code})")
