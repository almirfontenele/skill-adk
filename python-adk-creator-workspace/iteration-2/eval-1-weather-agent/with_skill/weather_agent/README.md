# weather_agent

A Gemini-powered agent that answers questions about current weather and forecasts using Google's Generative AI SDK (ADK 2.0).

## Getting Started

### 1. Clone / navigate to the project

```bash
cd weather_agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env` and add your Google API key:

```bash
cp .env.example .env
# edit .env and set GOOGLE_API_KEY=<your key>
```

Get a key at https://aistudio.google.com/app/apikey.

## Running the Agent

```bash
python main.py
```

The script runs two demo questions and then enters an interactive chat loop. Type `quit` or `exit` to stop.

## Adding Tools

1. Open `src/tools/core_tools.py`.
2. Add a new Python function with a clear docstring and type hints — the SDK uses these for automatic function calling.
3. Import the function in `main.py` and add it to the `tools` list when creating `GeminiAgent`.

Example:

```python
def get_air_quality(city: str) -> str:
    """Get the current air quality index for a city."""
    # your implementation here
    return "AQI: 42 (Good)"
```

## Project Structure

```
weather_agent/
├── src/
│   ├── agents/base_agent.py    # Generic GeminiAgent class
│   ├── tools/core_tools.py     # Weather tool functions
│   ├── schemas/types.py        # Pydantic models
│   └── config.py               # API key loading
├── main.py                     # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

## API Reference

- Google Generative AI SDK: https://googleapis.github.io/python-genai/
- Gemini API docs: https://ai.google.dev/gemini-api/docs
