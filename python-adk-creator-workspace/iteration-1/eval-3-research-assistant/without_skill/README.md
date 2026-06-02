# Research Assistant

A production-ready Python research assistant using Google Generative AI SDK with web search and content summarization capabilities.

## Features

- **Web Search**: Search the internet for information on any topic
- **Content Summarization**: Automatically summarize long content to a specified length
- **Page Fetching**: Extract text content from web pages
- **Function Calling**: Uses Google Generative AI SDK's function calling to dynamically invoke tools
- **Interactive Mode**: Run queries interactively or programmatically
- **Production-Ready**: Includes configuration management, error handling, and testing

## Project Structure

```
research_assistant/
├── research_assistant/           # Main package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Entry point
│   ├── agent.py                 # Research agent implementation
│   ├── config.py                # Configuration management
│   ├── tools.py                 # Tool definitions (search, summarization, fetch)
│   └── examples/                # Example scripts
│       ├── basic_research.py    # Basic usage example
│       └── custom_tools.py      # Custom tool usage example
├── tests/                       # Test suite
│   ├── test_agent.py           # Agent tests
│   └── test_tools.py           # Tool tests
├── .env.example                 # Example environment configuration
├── .gitignore                   # Git ignore rules
├── pyproject.toml              # Project metadata and dependencies
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. **Clone the repository** (or create the project):
```bash
cd /path/to/research_assistant
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
```
Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
MODEL=gemini-2.5-flash
MAX_SEARCH_RESULTS=5
SUMMARIZATION_LENGTH=500
```

## Usage

### Interactive Mode

```bash
python -m research_assistant.main --interactive
```

This starts an interactive session where you can type research queries:
```
Research query: What are the latest advances in AI?
Processing...
Result: [AI research findings...]
```

### Single Query

```bash
python -m research_assistant.main "What is machine learning?"
```

### Programmatic Usage

```python
from research_assistant.agent import ResearchAgent

agent = ResearchAgent()
result = agent.research("What are quantum computers?")
print(result)
```

## Available Tools

### 1. **web_search(query, num_results)**
Search the web for information on a topic.

```python
agent.tool_handlers['web_search'](
    query="machine learning",
    num_results=5
)
```

### 2. **summarize_content(content, length)**
Summarize provided content to a specified word length.

```python
agent.tool_handlers['summarize_content'](
    content="Long text here...",
    length=200
)
```

### 3. **fetch_page(url)**
Fetch and extract text content from a web page.

```python
agent.tool_handlers['fetch_page'](
    url="https://example.com"
)
```

## Configuration

Configuration is managed through environment variables and the `Config` class:

- **GOOGLE_API_KEY**: Your Google Generative AI API key (required)
- **MODEL**: Model to use (default: `gemini-2.5-flash`)
- **MAX_SEARCH_RESULTS**: Maximum search results to return (default: 5)
- **SEARCH_TIMEOUT**: Timeout for search requests in seconds (default: 10)
- **SUMMARIZATION_LENGTH**: Default summary length in words (default: 500)

### Development vs Production

The project includes separate configs:

```python
from research_assistant.config import get_config

# Development configuration
dev_config = get_config("development")

# Production configuration
prod_config = get_config("production")
```

## Examples

### Example 1: Basic Research

```python
from research_assistant.agent import ResearchAgent

agent = ResearchAgent()

# Research a topic
result = agent.research("What are the benefits of renewable energy?")
print(result)
```

### Example 2: Using Individual Tools

```python
from research_assistant.tools import WebSearchTool, ContentSummarizerTool
from research_assistant.config import Config

config = Config()

# Search for information
search_tool = WebSearchTool(config)
results = search_tool.search("artificial intelligence trends")

# Summarize content
summarizer = ContentSummarizerTool(config)
summary = summarizer.summarize(
    "Long text content here...",
    length=200
)
```

### Example 3: Run Examples

```bash
# Basic research example
python -m research_assistant.examples.basic_research

# Custom tools example
python -m research_assistant.examples.custom_tools
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=research_assistant
```

## API Details

### ResearchAgent

The main agent class that coordinates research tasks:

```python
class ResearchAgent:
    def research(self, query: str, use_tools: bool = True) -> str:
        """Perform research on a query using available tools."""
        
    def interactive_session(self) -> None:
        """Start an interactive research session."""
```

### Tool System

All tools follow a consistent pattern:

```python
class CustomTool:
    def get_function_declaration(self) -> types.FunctionDeclaration:
        """Return tool definition for the model."""
    
    def execute(self, **kwargs) -> dict:
        """Execute the tool with given arguments."""
```

## Google Generative AI SDK Integration

This project uses the Google Gen AI Python SDK with function calling:

```python
from google.genai import Client, types

client = Client(api_key="...")

# Define tools
tool = types.Tool(
    function_declarations=[...]
)

# Generate content with tools
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your query",
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)
```

The agent handles:
- Automatic function invocation
- Tool result processing
- Multi-turn conversations with tools
- Error handling for tool execution

## Error Handling

The agent includes comprehensive error handling:

```python
# Configuration validation
Config.validate()  # Raises ValueError if API key not set

# Tool execution errors
result = agent._execute_tool("web_search", args)
if "error" in result:
    print(f"Tool error: {result['error']}")

# Research errors
result = agent.research("query")  # Returns error message string
```

## Production Deployment

For production use:

1. **Use managed search API**: Replace `WebSearchTool` implementation with actual API (Google Custom Search, SerpAPI, Brave Search)
2. **Add caching**: Implement caching for search results and summaries
3. **Rate limiting**: Add rate limiting for API calls
4. **Monitoring**: Add logging and monitoring
5. **Security**: Use secrets management for API keys
6. **Testing**: Expand test coverage with integration tests

## Troubleshooting

### "GOOGLE_API_KEY environment variable is not set"
Set your API key in the `.env` file or environment variables.

### "Tool execution failed"
Check that the tool handler exists and the arguments are correct.

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Contributing

1. Create a feature branch
2. Add tests for new functionality
3. Run `pytest` to ensure tests pass
4. Submit a pull request

## License

MIT License

## Support

For issues or questions, please refer to:
- [Google Generative AI SDK Documentation](https://googleapis.github.io/python-genai/)
- [Gemini API Documentation](https://ai.google.dev/docs)
