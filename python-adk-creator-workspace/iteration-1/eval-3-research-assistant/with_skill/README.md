# Research Assistant

A powerful research tool built with Google's Generative AI SDK (Gemini 2.5 Flash). This project demonstrates how to build intelligent agents with automatic function calling for web search and content summarization.

## Features

- **Gemini-Powered Agent**: Uses the latest Gemini 2.5 Flash model with automatic function calling
- **Web Search**: Search the web for information on any topic
- **Content Summarization**: Automatically summarize long-form content
- **Conversation History**: Maintains context across multiple questions
- **Production-Ready Structure**: Clean, modular codebase with type hints and error handling

## Project Structure

```
research_assistant/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── base_agent.py          # ResearchAgent class
│   ├── tools/
│   │   ├── __init__.py
│   │   └── core_tools.py          # Web search & summarization tools
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── types.py               # Pydantic models
│   ├── __init__.py
│   └── config.py                  # Configuration & API client
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
├── .gitignore
└── README.md
```

## Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- A Google API key with Generative AI access

### 2. Setup

Clone or copy this project:

```bash
cd research_assistant
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:

```
GOOGLE_API_KEY=your-actual-api-key-here
```

Get your API key from: https://aistudio.google.com/app/apikey

### 4. Run the Assistant

Start the interactive research assistant:

```bash
python main.py
```

Or run in demo mode with pre-defined queries:

```bash
python main.py --demo
```

## Usage Examples

### Interactive Mode

```
Research Assistant - Powered by Gemini 2.5 Flash
============================================================

This assistant can search the web and summarize content.
Type 'quit' or 'exit' to end the conversation.

Research Agent initialized successfully!

You: What are the latest AI trends in 2024?
Assistant: [Provides comprehensive response with search results and summaries]

You: Can you summarize that for me?
Assistant: [Provides a concise summary]

You: exit
Thank you for using the Research Assistant. Goodbye!
```

### Programmatic Usage

```python
from src.agents import ResearchAgent

# Create agent
agent = ResearchAgent()

# Ask questions
response = agent.chat("What is machine learning?")
print(response)

# Clear history when needed
agent.clear_history()

# Use custom system prompt
agent.set_system_prompt("You are an expert technology analyst...")
```

## Adding Custom Tools

To add new tools, create functions in `src/tools/core_tools.py`:

```python
def my_tool(param1: str, param2: int = 10) -> str:
    """Tool description for Gemini to understand when to use it.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        str: The tool result
    """
    # Implementation
    return result
```

Then pass the tool to ResearchAgent:

```python
from src.tools.core_tools import my_tool

agent = ResearchAgent(tools=[my_tool, search_web, summarize_content])
```

## Advanced Configuration

### Custom System Prompt

```python
agent = ResearchAgent(
    system_prompt="You are a specialized research analyst in technology..."
)
```

### Using Different Models

```python
agent = ResearchAgent(model="gemini-2.0-pro")  # For more capable reasoning
```

### Structured Outputs with Pydantic

Use the models in `src/schemas/types.py` for structured data:

```python
from src.schemas.types import SearchQuery
from src.tools.core_tools import search_web

query = SearchQuery(query="AI trends", max_results=10)
results = search_web(query.query, query.max_results)
```

## API Reference

### ResearchAgent

Main agent class for conducting research.

**Constructor:**
```python
ResearchAgent(
    model: str = "gemini-2.5-flash",
    system_prompt: Optional[str] = None,
    tools: Optional[list[Callable]] = None
)
```

**Methods:**

- `chat(user_prompt: str) -> str`: Send a message and get a response
- `clear_history() -> None`: Clear conversation history
- `set_system_prompt(prompt: str) -> None`: Update system prompt

### Tools

**search_web(query: str, max_results: int = 5) -> str**
- Searches the web for information
- Returns formatted results with titles, URLs, and snippets

**summarize_content(content: str, max_length: int = 200) -> str**
- Summarizes provided text content
- Preserves key information in concise form

## Troubleshooting

### "GOOGLE_API_KEY not found"

**Solution:**
1. Check that `.env` file exists in the project root
2. Verify the `GOOGLE_API_KEY=` line is present
3. Ensure no spaces around the equals sign
4. Restart your Python environment

### "google-genai not installed"

**Solution:**
```bash
pip install -r requirements.txt
```

### "Module not found" errors

**Solution:**
- Ensure you're running from the project root: `cd /path/to/research_assistant`
- The script should be run as: `python main.py`

### API Rate Limits

If you hit rate limits:
1. Add delays between requests
2. Reduce batch sizes
3. Check your Google Cloud usage quota

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Generative AI API key | Yes |

## Dependencies

- **google-genai** (0.1.0): Google Generative AI SDK
- **pydantic** (>=2.0): Data validation and serialization
- **python-dotenv** (>=1.0.0): Environment variable management
- **requests** (>=2.31.0): HTTP library for future API integrations

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style

This project uses:
- Type hints throughout for better code clarity
- Clear docstrings following Google style
- Clean separation of concerns

### Extending the Project

1. **Add new tools**: Implement functions in `src/tools/`
2. **Create specialized agents**: Subclass `ResearchAgent` in `src/agents/`
3. **Add structured outputs**: Define Pydantic models in `src/schemas/`
4. **Implement persistence**: Add database models and queries

## Production Deployment

For production use:

1. **Secure API Keys**: Use a secrets manager (AWS Secrets Manager, HashiCorp Vault)
2. **Error Handling**: Add comprehensive logging and error recovery
3. **Rate Limiting**: Implement request throttling and caching
4. **Monitoring**: Add performance metrics and usage tracking
5. **Async Support**: Extend agent to support async/await for concurrent requests

Example production setup:

```python
import logging
from src.agents import ResearchAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

agent = ResearchAgent()

try:
    response = agent.chat("research query")
    logger.info(f"Query successful: {response[:100]}...")
except Exception as e:
    logger.error(f"Query failed: {e}")
```

## Performance Optimization

- **Caching**: Add response caching for repeated queries
- **Async Processing**: Use asyncio for parallel tool execution
- **Model Selection**: Choose models based on latency/capability trade-offs
- **Prompt Engineering**: Refine system prompts for faster, better responses

## License

This project is provided as-is for educational and development purposes.

## Support

For issues with the Gemini API or SDK:
- Official Docs: https://ai.google.dev/
- Python SDK: https://github.com/google/generative-ai-python
- Community: https://github.com/google/generative-ai-python/discussions

For issues with this project, review the Troubleshooting section above.
