# Calculator Bot - Complete Project Index

## Project Overview

**Name**: calculator_bot  
**Type**: Python ADK 2.0 (Google Generative AI Agent)  
**Purpose**: Math assistant that performs arithmetic operations using Gemini API  
**Status**: Production Ready  
**Version**: 1.0.0  
**Total Lines**: 1,413 (code + documentation)

## Document Guide

Start here based on your needs:

### For Getting Started
- **QUICK_START.md** (5 min read) - 30-second setup and basic usage
- **README.md** (15 min read) - Full documentation with examples

### For Understanding the Project
- **PROJECT_SUMMARY.md** (20 min read) - Architecture, components, and extensibility
- **PROJECT_TREE.txt** (10 min read) - Visual structure and execution flow
- **INDEX.md** (this file) - Navigation and reference

### For Coding
- main.py - Entry point and usage examples
- src/agents/base_agent.py - Core GeminiAgent class
- src/tools/core_tools.py - Calculator functions (add, subtract, multiply, divide)
- src/config.py - Environment and API configuration

## File Directory

```
calculator_bot/
├── QUICK_START.md              ← Start here!
├── README.md                   ← Full documentation
├── PROJECT_SUMMARY.md          ← Architecture overview
├── PROJECT_TREE.txt            ← Visual structure
├── INDEX.md                    ← This file
│
├── main.py                     ← Run this to start
├── requirements.txt            ← Dependencies
├── .env.example                ← API key template
├── .gitignore                  ← Git configuration
│
└── src/
    ├── config.py               ← API setup
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── base_agent.py       ← GeminiAgent class
    ├── tools/
    │   ├── __init__.py
    │   └── core_tools.py       ← Calculator functions
    └── schemas/
        ├── __init__.py
        └── types.py            ← Data models
```

## Quick Navigation

### Step 1: Setup (5 minutes)
1. Read: QUICK_START.md
2. Run: `cp .env.example .env`
3. Add your API key to `.env`
4. Run: `pip install -r requirements.txt`
5. Run: `python main.py`

### Step 2: Understanding (15 minutes)
1. Read: README.md "Features" and "Project Structure"
2. Read: PROJECT_SUMMARY.md "Key Components"
3. Skim: main.py to see example usage

### Step 3: Customization (30 minutes)
1. Edit: main.py system_prompt
2. Modify: src/tools/core_tools.py to add new functions
3. Run: Test with `python main.py`

### Step 4: Extension (1-2 hours)
1. Read: PROJECT_SUMMARY.md "Extensibility"
2. Add new tools to src/tools/
3. Implement custom agent behaviors
4. Create REST API wrapper

## Key Code Files

### main.py (Entry Point)
**Purpose**: Example usage and interactive mode  
**Lines**: ~120  
**Key Functions**:
- `main()` - Initializes agent, runs examples, starts interactive loop
- Error handling for API key and dependencies

**Example Usage**:
```bash
python main.py
```

**What it does**:
1. Initializes GeminiAgent with [add, subtract, multiply, divide]
2. Runs 4 example queries
3. Starts interactive chat mode
4. Handles user input and displays responses

### src/agents/base_agent.py (Core Agent)
**Purpose**: Main agent implementation with function calling  
**Lines**: ~130  
**Key Class**: GeminiAgent
**Methods**:
- `__init__(tools, system_prompt)` - Initialize agent
- `chat(user_message)` - Send message and get response
- `add_tool(tool)` - Register new tools dynamically
- `clear_history()` - Reset conversation
- `get_history()` - Retrieve conversation history

**How it works**:
1. Takes list of callable tools
2. Sends user message + tools to Gemini API
3. Gemini automatically calls appropriate tool
4. Returns response to user

### src/tools/core_tools.py (Calculator Functions)
**Purpose**: Arithmetic operations  
**Lines**: ~85  
**Functions**:
- `add(a, b)` - Addition
- `subtract(a, b)` - Subtraction
- `multiply(a, b)` - Multiplication
- `divide(a, b)` - Division (with zero check)

**Key Features**:
- Full type hints (Union[int, float])
- Comprehensive docstrings
- Examples in docstrings
- Error handling (divide by zero)

### src/config.py (Configuration)
**Purpose**: API setup and environment management  
**Lines**: ~60  
**Key Functions**:
- `get_api_key()` - Load GOOGLE_API_KEY from .env
- `get_client()` - Initialize Google Generative AI client
- `MODEL_ID = "gemini-2.5-flash"`

### src/schemas/types.py (Data Types)
**Purpose**: Data model definitions  
**Lines**: ~20  
**Classes**:
- `CalculationResult` - Represents operation results

## Quick Reference

### Run the Bot
```bash
python main.py
```

### Use as Library
```python
from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide

agent = GeminiAgent(tools=[add, subtract, multiply, divide])
response = agent.chat("What is 10 plus 5?")
print(response)
```

### Add New Tool
```python
# In src/tools/core_tools.py
def power(base, exp):
    """Raise base to the power of exp."""
    return base ** exp

# In main.py
from src.tools import power
agent.add_tool(power)
```

### Customize System Prompt
```python
# In main.py
agent = GeminiAgent(
    tools=[add, subtract, multiply, divide],
    system_prompt="You are an expert mathematician..."
)
```

## Feature Matrix

| Feature | File | Status |
|---------|------|--------|
| Natural Language Math | main.py, base_agent.py | ✓ |
| Add Numbers | core_tools.py | ✓ |
| Subtract Numbers | core_tools.py | ✓ |
| Multiply Numbers | core_tools.py | ✓ |
| Divide Numbers | core_tools.py | ✓ |
| Automatic Function Calling | base_agent.py | ✓ |
| Conversation History | base_agent.py | ✓ |
| Error Handling | config.py, main.py | ✓ |
| Interactive Mode | main.py | ✓ |
| API Configuration | config.py | ✓ |
| Environment Variables | config.py | ✓ |
| Type Hints | All files | ✓ |
| Docstrings | All functions | ✓ |

## Dependencies

```
google-genai==0.1.0      # Google Generative AI SDK
pydantic>=2.0            # Data validation
python-dotenv>=1.0.0     # Environment variables
```

**Install**: `pip install -r requirements.txt`

## Testing Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file created with API key
- [ ] `python main.py` runs without errors
- [ ] Example queries return correct results
- [ ] Interactive mode accepts input
- [ ] Can ask custom math questions
- [ ] Conversation history works
- [ ] Error handling works (e.g., division by zero)

## Common Tasks

### Change Bot Behavior
Edit `main.py` line ~55:
```python
system_prompt="You are a helpful math assistant..."  # Change this
```

### Add More Operations
1. Edit `src/tools/core_tools.py`
2. Add function with docstring
3. Import in `main.py`
4. Add to agent.tools list

### Save Conversation
Use `agent.get_history()` to retrieve all messages:
```python
history = agent.get_history()
# Save to file/database
import json
with open('conversation.json', 'w') as f:
    json.dump(history, f)
```

### Web Interface
Wrap agent in Flask/FastAPI:
```python
from flask import Flask, request, jsonify
from src.agents import GeminiAgent

app = Flask(__name__)
agent = GeminiAgent(tools=[...])

@app.route('/calculate', methods=['POST'])
def calculate():
    message = request.json['message']
    response = agent.chat(message)
    return jsonify({'response': response})
```

## Troubleshooting

**Problem**: API key not found
- **Solution**: Check .env file exists and has GOOGLE_API_KEY=

**Problem**: google-genai not installed
- **Solution**: Run `pip install -r requirements.txt`

**Problem**: Module not found
- **Solution**: Run from project root, ensure venv activated

**Problem**: Division by zero
- **Solution**: This is handled; agent will report the error

**Problem**: Model returns unexpected results
- **Solution**: Try rephrasing question or adjust system_prompt

## Architecture Overview

```
User Input
    ↓
main.py
    ↓
GeminiAgent.chat()
    ↓
Prepare messages with system prompt
    ↓
Call Gemini 2.5 Flash API with tools
    ↓
Gemini determines which tool to call
    ↓
Execute: add(), subtract(), multiply(), or divide()
    ↓
Gemini formats response
    ↓
Return to user via interactive loop
```

## Next Steps

1. **Immediate**: Run `python main.py` to verify setup
2. **Short-term**: Modify system_prompt and test
3. **Medium-term**: Add power() and sqrt() functions
4. **Long-term**: Create web interface or deploy to cloud

## Resources

- **Google AI Docs**: https://ai.google.dev/
- **Python SDK**: https://github.com/googleapis/python-genai
- **Gemini API**: https://aistudio.google.com/
- **Project README**: See README.md

## Support

**For questions about**:
- Setup → See QUICK_START.md
- Features → See README.md
- Architecture → See PROJECT_SUMMARY.md
- Structure → See PROJECT_TREE.txt
- Code → Read source files with comments

## Summary

This is a production-ready Python ADK 2.0 project that:
- Uses Google's Gemini API for intelligent responses
- Implements automatic function calling for calculations
- Provides both CLI and library usage
- Includes comprehensive documentation
- Follows Python best practices
- Is easily extensible for new features

**Start with**: QUICK_START.md (5 minutes)  
**Then explore**: README.md (15 minutes)  
**Finally code**: main.py and src/ (ongoing)

---

**Created**: 2026-06-01  
**Version**: 1.0.0  
**Status**: Ready for Production
