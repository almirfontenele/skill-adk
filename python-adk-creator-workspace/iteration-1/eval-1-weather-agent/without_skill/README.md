# Weather Agent

A production-ready Python weather agent powered by Google's Generative AI (Gemini 2.0) with function calling capabilities. The agent can answer questions about current weather and forecasts using natural language.

## Features

- **Gemini 2.0 Integration**: Uses Google's latest Gemini model for intelligent responses
- **Function Calling**: Automatically calls weather tools based on user queries
- **Multiple Weather Tools**:
  - Get current weather for any location
  - Get multi-day weather forecasts
  - Compare weather between two locations
  - Retrieve weather alerts
- **Type Safety**: Full type hints and Pydantic models for data validation
- **Production-Ready**: Proper error handling, logging, and configuration management
- **Extensible Architecture**: Easy to add new tools and weather data sources

## Project Structure

```
weather_agent/
├── src/
│   └── weather_agent/
│       ├── __init__.py           # Package initialization
│       ├── agent.py              # Main WeatherAgent class
│       ├── config.py             # Configuration management
│       ├── models.py             # Pydantic data models
│       └── tools.py              # Weather tools implementation
├── main.py                       # Entry point with demo
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Installation

1. **Clone or download the project**
   ```bash
   cd weather_agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: Google Generative AI API Key
# Get it from: https://ai.google.dev/
GOOGLE_API_KEY=your_api_key_here

# Optional: Weather API Key (for real weather data integration)
WEATHER_API_KEY=your_weather_api_key_here

# Optional: Model to use (default: gemini-2.0-flash)
GEMINI_MODEL=gemini-2.0-flash
```

## Usage

### Basic Usage

```python
from src.weather_agent import WeatherAgent

# Initialize the agent
agent = WeatherAgent()

# Ask a question
response = agent.answer_question("What's the weather in San Francisco?")
print(response.response)
```

### Direct Tool Access

```python
from src.weather_agent import WeatherAgent

agent = WeatherAgent()

# Get current weather
weather = agent.get_current_weather("Paris")
print(weather)

# Get forecast
forecast = agent.get_forecast("London", days=7)
print(forecast)
```

### Running the Demo

```bash
python main.py
```

This will run example queries and then enter interactive mode where you can ask your own questions.

## Available Tools

### 1. Get Current Weather
Retrieves current weather conditions for a location.

```python
{
    "name": "get_current_weather",
    "parameters": {
        "location": "City name or location"
    }
}
```

### 2. Get Weather Forecast
Retrieves multi-day weather forecast.

```python
{
    "name": "get_weather_forecast",
    "parameters": {
        "location": "City name or location",
        "days": 5  # Number of forecast days (1-14, default: 5)
    }
}
```

### 3. Compare Weather
Compares current weather between two locations.

```python
{
    "name": "compare_weather",
    "parameters": {
        "location1": "First city",
        "location2": "Second city"
    }
}
```

### 4. Get Weather Alerts
Retrieves any active weather alerts for a location.

```python
{
    "name": "get_weather_alerts",
    "parameters": {
        "location": "City name or location"
    }
}
```

## API Response Models

### WeatherData
```python
{
    "location": "San Francisco",
    "temperature": 20.5,
    "condition": "Partly Cloudy",
    "humidity": 65,
    "wind_speed": 12.5,
    "feels_like": 19.0
}
```

### WeatherForecast
```python
{
    "location": "London",
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
```

### AgentResponse
```python
{
    "query": "What's the weather in Paris?",
    "response": "The current weather in Paris is...",
    "weather_data": {...},
    "forecast": {...},
    "tool_calls": ["get_current_weather"]
}
```

## Extending the Agent

### Adding a New Tool

1. Add the tool function to `src/weather_agent/tools.py`:
```python
@staticmethod
def get_air_quality(location: str) -> Dict[str, Any]:
    """Get air quality for a location."""
    # Implementation here
    return {"status": "success", "data": {...}}
```

2. Add it to the `get_all_tools()` method

3. Update `agent.py` to include it in tool definitions and `_execute_tool()`

### Integrating Real Weather API

Replace the simulated weather data in `tools.py` with real API calls:

```python
import requests

def get_current_weather(location: str) -> Dict[str, Any]:
    """Get current weather using real API."""
    api_key = Config.WEATHER_API_KEY
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={"q": location, "appid": api_key}
    )
    # Process and return data
```

## Error Handling

The agent includes comprehensive error handling:

- Configuration validation on startup
- Graceful API error handling with logging
- Invalid tool call handling
- User input validation

All errors are logged to the console with detailed information.

## Logging

Logging is configured to show:
- Timestamp
- Logger name
- Log level
- Message

View logs in the console output when running the agent.

## Dependencies

- **google-genai**: Official Google Generative AI SDK
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation with type hints
- **requests**: HTTP library (optional, for real API integration)

## Production Considerations

For production deployment:

1. **Use a secrets manager** for API keys (AWS Secrets Manager, Google Secret Manager, etc.)
2. **Add rate limiting** to prevent excessive API calls
3. **Implement caching** for frequent queries
4. **Add monitoring and alerting** for failures
5. **Use a database** to store weather history
6. **Implement authentication** if exposing as a service
7. **Add request validation** for API endpoints
8. **Test extensively** with edge cases and error scenarios

## Testing

Example test structure:

```python
import pytest
from src.weather_agent import WeatherAgent

def test_agent_initialization():
    agent = WeatherAgent()
    assert agent.model is not None

def test_answer_question():
    agent = WeatherAgent()
    response = agent.answer_question("What's the weather?")
    assert response.response is not None
```

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the configuration
2. Verify your Google API key is valid
3. Check the logs for error details
4. Review the Gemini API documentation

## Resources

- [Google Generative AI SDK](https://github.com/googleapis/python-genai)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
