# Calculator Bot - Project Summary

## Overview

**Project Name**: calculator_bot  
**Description**: A math assistant bot that helps users do math operations including add, subtract, multiply, and divide using Gemini  
**Framework**: Python ADK 2.0 (Google Generative AI SDK)  
**Model**: Gemini 2.5 Flash  
**Creation Date**: 2026-06-01

## Project Structure

```
calculator_bot/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── base_agent.py              # Core GeminiAgent class
│   ├── tools/
│   │   ├── __init__.py
│   │   └── core_tools.py              # Calculator functions
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── types.py                   # Data type definitions
│   ├── __init__.py
│   └── config.py                      # Configuration & API setup
├── main.py                            # Entry point & examples
├── requirements.txt                   # Dependencies
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
└── README.md                          # Full documentation
```

## Key Components

### 1. Configuration (`src/config.py`)
- Loads environment variables from `.env`
- Initializes Google Generative AI client
- Defines model ID: `gemini-2.5-flash`
- Validates API key presence

### 2. Base Agent (`src/agents/base_agent.py`)
The `GeminiAgent` class provides:
- Initialization with callable tools
- `chat(user_message)` method for generating responses
- Automatic function calling via Gemini API
- Conversation history tracking
- System prompt support for behavior guidance
- Error handling for API failures

**Key Methods**:
- `chat(user_message: str) -> str`: Send a message and receive response
- `add_tool(tool: Callable)`: Register new tools dynamically
- `clear_history()`: Reset conversation
- `get_history()`: Retrieve conversation history
- `_prepare_messages()`: Format messages with system prompt

### 3. Calculator Tools (`src/tools/core_tools.py`)
Four arithmetic functions with full docstrings:

```python
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    """Add two numbers together."""

def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    """Subtract one number from another."""

def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    """Multiply two numbers together."""

def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    """Divide one number by another. Raises ValueError if b is 0."""
```

All functions:
- Include type hints for parameters and return values
- Have comprehensive docstrings
- Include example usage in docstrings
- Support both int and float operands
- Are designed for automatic function calling by Gemini

### 4. Data Types (`src/schemas/types.py`)
`CalculationResult` dataclass for representing operation results:
- Stores operation name, operands, and result
- Optional error field for error handling
- String representation for easy display

### 5. Entry Point (`main.py`)
Comprehensive example script that:
- Initializes the agent with all calculator tools
- Runs predefined example queries (add, divide, complex operations)
- Provides interactive mode for user input
- Includes proper error handling
- Guides users through setup issues

**Example Workflow**:
1. Load environment configuration
2. Initialize GeminiAgent with [add, subtract, multiply, divide]
3. Send user queries: "What is 25 plus 17?"
4. Agent automatically calls appropriate tools
5. Returns computed results with explanation

## Dependencies

```
google-genai==0.1.0      # Google Generative AI SDK
pydantic>=2.0            # Data validation & type hints
python-dotenv>=1.0.0     # Environment variable management
```

## Setup Instructions

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your Google API key
nano .env
```

Add to `.env`:
```
GOOGLE_API_KEY=your-actual-api-key-here
```

### 3. Running the Bot
```bash
# Run with example queries and interactive mode
python main.py
```

## Usage Examples

### As a Standalone Script
```bash
$ python main.py

============================================================
Calculator Bot - Powered by Gemini
============================================================

Agent initialized successfully with calculator tools!

Running example queries...
--------------------------------------------

Query 1: What is 25 plus 17?
Response: The answer is 42.

...
```

### As a Library
```python
from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide

# Create agent
agent = GeminiAgent(tools=[add, subtract, multiply, divide])

# Ask questions
response = agent.chat("What is 100 divided by 4?")
print(response)  # "The result is 25."

# Add dynamic tools
from src.tools import power
agent.add_tool(power)

# Continue conversation
response = agent.chat("Now square that result")
print(response)  # "25 squared is 625."
```

## How Automatic Function Calling Works

1. **User sends**: "What is 20 multiplied by 5?"
2. **Agent passes to Gemini**: message + tools=[multiply, add, subtract, divide]
3. **Gemini determines**: multiply function needed with args (20, 5)
4. **Gemini calls**: multiply(20, 5) → returns 100
5. **Agent presents**: "The result is 100."

This happens automatically without explicit function invocation code.

## Features Implemented

- ✅ Natural language math queries
- ✅ Automatic function calling with Gemini
- ✅ Four arithmetic operations (add, subtract, multiply, divide)
- ✅ Error handling (division by zero, API failures)
- ✅ Conversation history tracking
- ✅ System prompt customization
- ✅ Dynamic tool registration
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Interactive mode with examples
- ✅ Environment configuration
- ✅ Production-ready structure

## Extensibility

### Adding New Operations
Edit `src/tools/core_tools.py`:
```python
def power(base: Union[int, float], exp: Union[int, float]) -> Union[int, float]:
    """Raise base to the power of exp."""
    return base ** exp

def square_root(n: Union[int, float]) -> float:
    """Calculate square root of n."""
    import math
    return math.sqrt(n)
```

### Registering New Tools
```python
from src.tools import power, square_root
agent = GeminiAgent(tools=[add, subtract, multiply, divide, power, square_root])
```

### Custom System Prompt
```python
agent = GeminiAgent(
    tools=[add, subtract, multiply, divide],
    system_prompt="You are an expert mathematician..."
)
```

## Error Handling

The project handles several error scenarios:

1. **Missing API Key**: Guides user to create `.env`
2. **Missing Dependencies**: Prompts `pip install -r requirements.txt`
3. **Module Not Found**: Checks working directory
4. **Division by Zero**: Raises ValueError in divide function
5. **API Failures**: Catches and displays errors gracefully

## Testing the Project

To verify the installation works:

```bash
# Run main.py which includes built-in tests
python main.py

# Expected output: Several example queries executed successfully
```

## Best Practices Implemented

1. **Configuration Management**: Centralized in `src/config.py`
2. **Type Hints**: All functions and methods
3. **Documentation**: Docstrings on all functions
4. **Error Handling**: Try-except blocks around API calls
5. **Separation of Concerns**: Agents, tools, schemas in separate modules
6. **Modularity**: Easy to add new tools and agent behaviors
7. **Standards**: PEP 8 compliant code formatting
8. **Security**: API key in environment variables, not hardcoded

## Next Steps for Users

1. **Run the bot**: `python main.py`
2. **Explore responses**: Try different math questions
3. **Add tools**: Extend with power, square_root, trigonometric functions
4. **Customize prompts**: Modify system_prompt in GeminiAgent
5. **Build UI**: Wrap agent in Flask/FastAPI web server
6. **Add persistence**: Store conversations in database
7. **Deploy**: Use Gemini API in production with proper error handling

## Troubleshooting

| Issue | Solution |
|-------|----------|
| GOOGLE_API_KEY not found | Create `.env` from `.env.example` and add your key |
| google-genai not installed | Run `pip install -r requirements.txt` |
| Module not found errors | Run from project root: `python main.py` |
| Division by zero error | The divide function handles this with ValueError |
| Unexpected model responses | Try rephrasing questions or adjust system_prompt |

## Files Generated

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Entry point and examples | ~120 |
| `src/config.py` | API initialization | ~60 |
| `src/agents/base_agent.py` | Core agent implementation | ~130 |
| `src/tools/core_tools.py` | Calculator functions | ~85 |
| `src/schemas/types.py` | Data type definitions | ~20 |
| `requirements.txt` | Dependencies | 3 |
| `.env.example` | Environment template | 1 |
| `.gitignore` | Git ignore rules | 30+ |
| `README.md` | Full documentation | 200+ |

**Total Implementation**: ~650 lines of production-ready code and documentation

## Model Configuration

- **Model ID**: `gemini-2.5-flash`
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Tools**: [add, subtract, multiply, divide]
- **Automatic Function Calling**: Enabled
- **API Version**: google-genai 0.1.0

## Support Resources

- [Google AI Python SDK](https://github.com/googleapis/python-genai)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/)
- Project README.md for detailed usage guide

---

**Status**: Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2026-06-01
