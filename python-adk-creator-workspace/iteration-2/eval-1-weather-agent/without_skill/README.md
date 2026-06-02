# Weather Agent

A production-ready conversational weather assistant powered by **Google Gemini** (via the `google-genai` Python SDK) and live data from the **Open-Meteo** API (free, no key required).

## Features

- Current weather conditions (temperature, humidity, wind, precipitation, condition)
- Multi-day forecast (1–16 days)
- Automatic function calling — Gemini decides when and how to invoke the tools
- Persistent conversation history across turns
- Zero-cost weather data via Open-Meteo

## Project Structure

```
weather_agent/
    __init__.py      # Public API
    agent.py         # WeatherAgent class
    tools.py         # get_current_weather, get_weather_forecast
main.py              # Interactive CLI REPL
tests/
    test_tools.py
    test_agent.py
pyproject.toml
.env.example
```

## Setup

1. **Clone / navigate to the project directory.**

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   # or with uv:
   uv sync
   ```

4. **Configure your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_API_KEY=<your key>
   ```
   Get a free key at <https://aistudio.google.com/app/apikey>.

5. **Load the env file:**
   ```bash
   export $(cat .env | xargs)
   ```

## Usage

### Interactive CLI

```bash
python main.py
```

```
Weather Agent - powered by Gemini
Type your weather questions below. Type 'quit' or 'exit' to stop.

You: What is the weather in Tokyo right now?
Agent: The current weather in Tokyo, Tokyo, Japan is mainly clear ...

You: Give me a 5-day forecast for the same city.
Agent: Here is the 5-day forecast for Tokyo ...

You: reset
Conversation history cleared.

You: exit
Goodbye!
```

### Programmatic API

```python
from weather_agent import WeatherAgent

agent = WeatherAgent()                        # reads GOOGLE_API_KEY from env

# One-shot question (no history)
print(agent.ask("Is it raining in Berlin?"))

# Conversational (history preserved across calls)
print(agent.chat("What is the weather in Sydney?"))
print(agent.chat("And the forecast for next week?"))

agent.reset()  # clear history
```

## Running Tests

```bash
pytest -v
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google AI Studio API key |
