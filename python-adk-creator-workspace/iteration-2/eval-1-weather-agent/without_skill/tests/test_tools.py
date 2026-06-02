"""Unit tests for weather tools."""

import pytest
from unittest.mock import patch, MagicMock

from weather_agent.tools import get_current_weather, get_weather_forecast, _wmo_description


# ---------------------------------------------------------------------------
# WMO description
# ---------------------------------------------------------------------------

def test_wmo_description_known_codes():
    assert _wmo_description(0) == "Clear sky"
    assert _wmo_description(3) == "Overcast"
    assert _wmo_description(95) == "Thunderstorm"


def test_wmo_description_unknown_code():
    assert "Unknown" in _wmo_description(999)


# ---------------------------------------------------------------------------
# get_current_weather
# ---------------------------------------------------------------------------

def _make_geocode_response():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {
        "results": [
            {"latitude": 51.5, "longitude": -0.12, "name": "London", "admin1": "England", "country": "UK"}
        ]
    }
    return mock


def _make_weather_response():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {
        "current": {
            "temperature_2m": 15.0,
            "apparent_temperature": 13.0,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 20.0,
            "wind_direction_10m": 270,
            "precipitation": 0.0,
            "weather_code": 1,
            "is_day": 1,
        },
        "current_units": {
            "temperature_2m": "°C",
            "apparent_temperature": "°C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
            "precipitation": "mm",
        },
    }
    return mock


def test_get_current_weather_success():
    with patch("weather_agent.tools.httpx.get") as mock_get:
        mock_get.side_effect = [_make_geocode_response(), _make_weather_response()]
        result = get_current_weather("London")

    assert "London" in result
    assert "15.0" in result
    assert "Mainly clear" in result


def test_get_current_weather_location_not_found():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {}  # no results key

    with patch("weather_agent.tools.httpx.get", return_value=mock):
        result = get_current_weather("NonexistentCity12345")

    assert "Error" in result


# ---------------------------------------------------------------------------
# get_weather_forecast
# ---------------------------------------------------------------------------

def _make_forecast_response():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {
        "daily": {
            "time": ["2026-06-01", "2026-06-02"],
            "weather_code": [0, 61],
            "temperature_2m_max": [20.0, 18.0],
            "temperature_2m_min": [12.0, 10.0],
            "precipitation_sum": [0.0, 5.2],
            "wind_speed_10m_max": [15.0, 22.0],
            "sunrise": ["2026-06-01T05:00", "2026-06-02T05:01"],
            "sunset": ["2026-06-01T21:00", "2026-06-02T20:59"],
        },
        "daily_units": {
            "temperature_2m_max": "°C",
            "precipitation_sum": "mm",
            "wind_speed_10m_max": "km/h",
        },
    }
    return mock


def test_get_weather_forecast_success():
    with patch("weather_agent.tools.httpx.get") as mock_get:
        mock_get.side_effect = [_make_geocode_response(), _make_forecast_response()]
        result = get_weather_forecast("London", days=2)

    assert "London" in result
    assert "2026-06-01" in result
    assert "Clear sky" in result
    assert "Slight rain" in result


def test_get_weather_forecast_clamps_days():
    """Days outside [1, 16] should be clamped."""
    with patch("weather_agent.tools.httpx.get") as mock_get:
        mock_get.side_effect = [_make_geocode_response(), _make_forecast_response()]
        # Pass 0 days — should be clamped to 1
        get_weather_forecast("London", days=0)
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["forecast_days"] == 1
