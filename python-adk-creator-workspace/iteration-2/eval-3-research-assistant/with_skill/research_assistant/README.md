# research_assistant

An AI-powered research assistant built with Google's Generative AI SDK (ADK 2.0). The agent can search the web, fetch page content, and summarize information using Gemini with automatic function calling.

## Getting Started

### 1. Clone / navigate to the project

```bash
cd research_assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env` and add your Google API key:

```bash
cp .env.example .env
# Edit .env and replace 'your-api-key-here' with your actual key
```

Get a free API key at: https://aistudio.google.com/app/apikey

## Running the Agent

```bash
python main.py
```

The demo will run two example queries and then open an interactive chat loop. Type `reset` to clear conversation history or `quit` to exit.

## Project Structure

```
research_assistant/
├── src/
│   ├── agents/
│   │   └── base_agent.py    # GeminiAgent — generic orchestration class
│   ├── tools/
│   │   └── core_tools.py    # search_web, summarize_content, get_page_content
│   ├── schemas/
│   │   └── types.py         # Pydantic models for structured data
│   └── config.py            # API key loading
├── main.py                  # Entry point
├── requirements.txt
└── .env.example
```

## Adding Tools

1. Open `src/tools/core_tools.py`
2. Add a new function with type hints and a docstring:

```python
def my_new_tool(param: str) -> str:
    """Brief description of what this tool does.

    Args:
        param: Description of the parameter.

    Returns:
        Description of the return value.
    """
    # your implementation
    return result
```

3. Import and pass it to `GeminiAgent` in `main.py`:

```python
from src.tools.core_tools import my_new_tool

agent = GeminiAgent(tools=[search_web, summarize_content, my_new_tool], ...)
```

The SDK will automatically call the function when the model decides to use it — no extra wiring needed.

## API Reference

- [Google Generative AI SDK (google-genai)](https://googleapis.github.io/python-genai/)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)
