# calculator_bot

A math assistant bot powered by Google Gemini that helps users perform arithmetic operations using natural language.

## Features

- Add, subtract, multiply, and divide numbers
- Conversational interface with history
- Automatic function calling via the Gemini API

## Getting Started

### 1. Clone or download the project

```bash
cd calculator_bot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up your API key

Copy `.env.example` to `.env` and add your Google API key:

```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY=your-actual-key
```

Get a free API key at: https://aistudio.google.com/app/apikey

## Running the Agent

```bash
python main.py
```

Example session:

```
You: What is 42 plus 18?
Bot: 42 plus 18 equals 60.

You: Now divide that by 4
Bot: 60 divided by 4 equals 15.

You: reset
Conversation history cleared.
```

## Adding Tools

Add new tool functions to `src/tools/core_tools.py`. Each function must have:

1. Type hints on all parameters and return value
2. A docstring describing what it does

```python
def square_root(n: float) -> float:
    """Returns the square root of a number."""
    import math
    return math.sqrt(n)
```

Then register it in `main.py`:

```python
from src.tools import add, subtract, multiply, divide, square_root

agent = GeminiAgent(tools=[add, subtract, multiply, divide, square_root], ...)
```

## Project Structure

```
calculator_bot/
├── src/
│   ├── agents/
│   │   └── base_agent.py    # Generic GeminiAgent class
│   ├── tools/
│   │   └── core_tools.py    # Math tool functions
│   ├── schemas/
│   │   └── types.py         # Pydantic models
│   └── config.py            # API key loading
├── main.py                  # Entry point
├── requirements.txt
└── .env.example
```

## API Reference

- [google-genai SDK docs](https://googleapis.github.io/python-genai/)
- [Gemini API reference](https://ai.google.dev/api)
