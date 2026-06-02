# Research Assistant - Project Overview

## Project Summary

A production-ready Python research assistant built with Google Generative AI SDK 2.0 featuring web search and content summarization tools. The project demonstrates advanced function calling capabilities, agent patterns, and tool integration with the Gemini API.

## Creation Method

This project was created **without using the python-adk-creator skill**, implementing all components manually following production best practices:

- Complete project structure with modular design
- Configuration management with environment variables
- Production-ready error handling
- Comprehensive testing framework
- Detailed documentation and examples

## Project Tree

```
research_assistant/
├── research_assistant/                    # Main package directory
│   ├── __init__.py                       # Package initialization (v0.1.0)
│   ├── main.py                           # CLI entry point with interactive mode
│   ├── agent.py                          # ResearchAgent - main orchestrator
│   ├── config.py                         # Configuration management (Dev/Prod)
│   ├── tools.py                          # Tool implementations (Search, Summarize, Fetch)
│   └── examples/
│       ├── __init__.py
│       ├── basic_research.py             # Basic research query examples
│       └── custom_tools.py               # Individual tool demonstrations
├── tests/                                # Test suite
│   ├── __init__.py
│   ├── test_agent.py                    # Agent unit tests
│   └── test_tools.py                    # Tool unit tests
├── .gitignore                            # Git ignore patterns
├── .env.example                          # Example environment configuration
├── pyproject.toml                        # Project metadata and build config
├── requirements.txt                      # Python dependencies
├── README.md                             # Comprehensive documentation
└── PROJECT_OVERVIEW.md                  # This file
```

## Key Components

### 1. **ResearchAgent** (`agent.py`)
The main orchestrator that coordinates research tasks using Google Generative AI SDK:

- Initializes Gemini 2.5 Flash model with function calling
- Manages tool definitions and execution
- Handles multi-turn conversations with tool results
- Supports both interactive and programmatic usage

Key methods:
- `research(query, use_tools=True)` - Perform research with tools
- `interactive_session()` - Interactive query loop
- `_process_function_calls()` - Handle model-invoked functions
- `_execute_tool()` - Execute specific tool with args

### 2. **Tool System** (`tools.py`)
Three specialized tools for research:

#### WebSearchTool
- Search the internet for information
- Configurable result limits
- Error handling for invalid queries
- Function declaration for Gemini API

#### ContentSummarizerTool
- Extractive summarization algorithm
- Target word length support
- Sentence-based content processing
- Performance metrics (original/summary length)

#### FetchPageTool
- Extract text from web pages
- HTML parsing with BeautifulSoup
- Content truncation for size limits
- User-Agent headers for compatibility

All tools implement:
- `get_function_declaration()` - Gemini API schema
- Error handling and validation
- Configuration-based parameters

### 3. **Configuration Management** (`config.py`)
Flexible configuration system:

- **Base Config**: Common settings
- **DevelopmentConfig**: Higher temperature (0.9), debug enabled
- **ProductionConfig**: Lower temperature (0.5), debug disabled
- **Environment variables**: API key, model, limits, timeouts
- **Validation**: Ensures required settings are present

### 4. **CLI Interface** (`main.py`)
Multiple usage modes:

- **Interactive mode** (`--interactive`): Loop of queries and responses
- **Single query mode**: Process one query and exit
- **Default mode**: Starts interactive session

## Dependencies

### Core
- `google-genai>=0.4.0` - Google Generative AI SDK with function calling
- `requests>=2.31.0` - HTTP requests for page fetching
- `beautifulsoup4>=4.12.0` - HTML parsing
- `python-dotenv>=1.0.0` - Environment variable management

### Development (optional)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=23.0.0` - Code formatter
- `isort>=5.12.0` - Import sorting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking

## Google Generative AI SDK Integration

### Function Calling Pattern

The project demonstrates Google's recommended function calling pattern:

```python
# 1. Define tool schemas
tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="web_search",
            description="Search the web...",
            parameters_json_schema={...}
        ),
        ...
    ]
)

# 2. Make request with tools
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=query,
    config=types.GenerateContentConfig(tools=[tool])
)

# 3. Process function calls
if response.function_calls:
    for call in response.function_calls:
        result = execute_tool(call.name, call.args)
        # ... send result back to model

# 4. Get final response
```

### Supported Models
- Primary: `gemini-2.5-flash` (fast, efficient)
- Compatible: `gemini-2.0-flash`, `gemini-1.5-pro`

## Configuration Examples

### Development Setup
```bash
cp .env.example .env
# Edit .env:
GOOGLE_API_KEY=your_key_here
MODEL=gemini-2.5-flash
TEMPERATURE=0.7
```

### Production Setup
```python
from research_assistant.config import get_config
config = get_config("production")
# Lower temperature (0.5), debug disabled
```

## Usage Examples

### 1. Interactive Research
```bash
python -m research_assistant.main --interactive
# Type queries and get responses with tool invocation
```

### 2. Programmatic Research
```python
from research_assistant.agent import ResearchAgent

agent = ResearchAgent()
result = agent.research("What are the latest AI trends?")
print(result)
```

### 3. Individual Tool Usage
```python
from research_assistant.tools import WebSearchTool
from research_assistant.config import Config

config = Config()
search = WebSearchTool(config)
results = search.search("quantum computing")
```

## Testing Strategy

### Test Coverage
- **Agent tests** (`test_agent.py`):
  - Initialization with config
  - Tool handler availability
  - Error handling for unknown tools

- **Tool tests** (`test_tools.py`):
  - Valid input handling
  - Error conditions (empty, None, invalid)
  - Function declaration generation
  - Custom parameter support

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=research_assistant

# Run specific test
pytest tests/test_tools.py::TestWebSearchTool::test_search_with_valid_query
```

## Production Considerations

### Recommended Enhancements

1. **Replace Mock Search**
   - Integrate real search API (SerpAPI, Google Custom Search, Brave)
   - Implement API key rotation
   - Add rate limiting

2. **Add Caching Layer**
   - Cache search results
   - Cache summarizations
   - Time-based cache invalidation

3. **Enhanced Error Handling**
   - Retry mechanisms with exponential backoff
   - Graceful degradation for failing tools
   - Detailed error logging

4. **Monitoring & Observability**
   - Request/response logging
   - Performance metrics
   - Error tracking

5. **Security**
   - Use secrets manager for API keys
   - Sanitize user inputs
   - Rate limiting per user/IP

6. **Scalability**
   - Async tool execution
   - Connection pooling
   - Load balancing for multiple agents

## File Descriptions

| File | Purpose |
|------|---------|
| `agent.py` | Core research agent with function calling |
| `tools.py` | Web search, summarization, and page fetching tools |
| `config.py` | Configuration management (Dev/Prod) |
| `main.py` | CLI entry point and interactive mode |
| `test_agent.py` | Unit tests for agent |
| `test_tools.py` | Unit tests for all tools |
| `examples/basic_research.py` | Example: Basic research queries |
| `examples/custom_tools.py` | Example: Direct tool usage |
| `pyproject.toml` | Project metadata and dependencies |
| `requirements.txt` | Python package dependencies |
| `README.md` | Full documentation |

## API Documentation

### ResearchAgent

```python
class ResearchAgent:
    def __init__(self, config: Optional[Config] = None)
        # Initialize with optional custom config
    
    def research(self, query: str, use_tools: bool = True) -> str
        # Perform research with optional tool usage
    
    def interactive_session(self) -> None
        # Start interactive query loop
    
    def _process_function_calls(response, user_message, config) -> str
        # Process model-generated function calls
    
    def _execute_tool(tool_name: str, tool_args: dict) -> dict
        # Execute named tool with arguments
```

### Tool Interfaces

All tools implement:
```python
def get_function_declaration() -> types.FunctionDeclaration
    # Return schema for Gemini API

def operation(param: str) -> dict[str, Any]
    # Execute operation, return result with error handling
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | (required) | Google Generative AI API key |
| `MODEL` | `gemini-2.5-flash` | Gemini model to use |
| `MAX_SEARCH_RESULTS` | `5` | Default search result limit |
| `SEARCH_TIMEOUT` | `10` | HTTP request timeout (seconds) |
| `SUMMARIZATION_LENGTH` | `500` | Default summary target length |
| `TEMPERATURE` | `0.7` | Model temperature (creativity) |
| `TOP_P` | `0.9` | Model top_p (diversity) |
| `MAX_TOKENS` | `2048` | Maximum response tokens |

## Known Limitations

1. **Mock Search Implementation**: Current web search uses placeholder data. For production, integrate real search API.
2. **No Caching**: Repeated queries will make new API calls.
3. **Synchronous Only**: Tools execute sequentially, not in parallel.
4. **Limited Content Parsing**: BeautifulSoup handles basic HTML; complex layouts may fail.
5. **No Authentication**: Search results are not personalized or authenticated.

## Next Steps

1. **Add Real Search API**: Replace mock search with actual implementation
2. **Implement Caching**: Add Redis or in-memory caching
3. **Async Support**: Make tools async-compatible
4. **Enhanced UI**: Add web interface or chat UI
5. **Multi-Agent**: Support agent collaboration
6. **Deployment**: Containerize with Docker for production

## Version History

- **0.1.0** (Current): Initial release with basic research tools
  - Google Generative AI SDK integration
  - Function calling support
  - Web search, summarization, page fetching
  - Interactive and programmatic interfaces
  - Comprehensive test coverage

## Support & Resources

- **Google Generative AI SDK**: https://googleapis.github.io/python-genai/
- **Gemini API Docs**: https://ai.google.dev/docs
- **Function Calling Guide**: https://ai.google.dev/docs/function_calling
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/
- **Python Best Practices**: https://pep8.org/

## Author Notes

This project was created as a reference implementation of:
- Production-ready Python project structure
- Google Generative AI SDK 2.0 integration
- Advanced function calling patterns
- Tool-using agent architecture
- Professional error handling and testing

Created without skill automation to showcase best practices in:
- Project organization
- Dependency management
- Configuration patterns
- Test-driven development
- Comprehensive documentation
