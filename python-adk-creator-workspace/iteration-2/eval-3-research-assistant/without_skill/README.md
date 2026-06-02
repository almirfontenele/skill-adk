# Research Assistant

An AI-powered research assistant built with the [Google GenAI Python SDK](https://github.com/googleapis/python-genai).  
It uses Gemini's automatic function-calling to orchestrate web searches and content summarization in a single, conversational interface.

## Features

- **Web search** — searches the web via DuckDuckGo (no key required) or Google Search via SerpAPI (optional, richer results)
- **Page fetching** — retrieves and cleans the full text of any URL
- **Summarization** — condenses long pages before feeding them back to the model
- **Multi-turn conversation** — remembers context across turns in the same session
- **CLI** — single-query mode or interactive REPL

## Quick Start

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY (required)
```

Then load the variables:

```bash
export $(grep -v '^#' .env | xargs)   # bash/zsh
# or use python-dotenv if preferred
```

### 3. Run

**Interactive mode:**

```bash
research-assistant
```

**Single query:**

```bash
research-assistant "What are the latest breakthroughs in quantum computing?"
```

**With options:**

```bash
research-assistant --model gemini-2.5-pro --max-results 8 "Explain diffusion models"
```

## Running Tests

```bash
pytest
# with coverage:
pytest --cov=research_assistant --cov-report=term-missing
```

## Project Structure

```
research_assistant/
  __init__.py      — package entry point
  config.py        — environment-based configuration
  tools.py         — callable tools: search_web, fetch_page_content, summarize_text
  agent.py         — ResearchAssistant class (GenAI client + automatic function calling)
  cli.py           — argparse CLI wiring
tests/
  test_tools.py
  test_agent.py
  test_config.py
pyproject.toml
.env.example
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Yes | — | Gemini API key from AI Studio |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Model ID to use |
| `SERPAPI_KEY` | No | — | SerpAPI key for Google Search |
| `MAX_SEARCH_RESULTS` | No | `5` | Max search results per query |
| `SUMMARY_MAX_WORDS` | No | `300` | Max words in auto-summaries |

## How It Works

1. The user sends a query.
2. `ResearchAssistant.research()` passes the full conversation history plus three tool functions to `client.models.generate_content`.
3. Gemini decides autonomously which tools to call and with what arguments (automatic function calling).
4. The SDK executes the Python functions, returns results to the model, and Gemini produces a final cited answer.
5. Both the user turn and the model turn are appended to `_history` for multi-turn support.

## License

MIT
