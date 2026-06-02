# Calculator Bot - Key Files Overview

## Project Deliverables

This document provides quick reference to the most important files in the calculator bot project.

---

## 1. Entry Point: main.py (46 lines)

**Purpose**: Application entry point that initializes and runs the calculator agent.

**Key Code**:
```python
from src.config import Config
from src.agent import CalculatorAgent

def main():
    Config.validate()  # Validate required API key
    agent = CalculatorAgent()
    agent.run_interactive()  # Start interactive mode
```

**What it does**:
- Validates configuration (checks for API key)
- Creates CalculatorAgent instance
- Starts interactive mode for user input

---

## 2. Agent Logic: src/agent.py (185 lines)

**Purpose**: Main agent implementation with Gemini function calling.

**Key Class**: `CalculatorAgent`

**Key Methods**:

### `interact(user_input: str) -> str`
Handles the complete function calling flow:
1. Takes user input
2. Creates tool schema in JSON format
3. Sends to Gemini with available tools
4. Gemini analyzes input and calls appropriate tool
5. Executes tool and returns result

**Example Flow**:
```python
response = self.client.models.generate_content(
    model=self.model_name,
    contents=user_input,
    config=types.GenerateContentConfig(tools=[tool_schema])
)

# Check if model made function calls
if response.function_calls:
    for function_call in response.function_calls:
        tool_name = function_call.name
        tool_args = dict(function_call.args)
        result = self.process_tool_call(tool_name, tool_args)
```

### `process_tool_call(tool_name, tool_args)`
Executes the actual tool and returns result.

### `run_interactive()`
CLI loop that accepts user input and displays responses.

---

## 3. Calculator Tools: src/tools/calculator.py (196 lines)

**Purpose**: Implements the four calculator functions and their tool definitions.

**Tool Functions**:

### `add(a: float, b: float) -> float`
```python
def add(a: float, b: float) -> float:
    result = a + b
    logger.info(f"Add operation: {a} + {b} = {result}")
    return result
```

### `subtract(a: float, b: float) -> float`
```python
def subtract(a: float, b: float) -> float:
    result = a - b
    logger.info(f"Subtract operation: {a} - {b} = {result}")
    return result
```

### `multiply(a: float, b: float) -> float`
```python
def multiply(a: float, b: float) -> float:
    result = a * b
    logger.info(f"Multiply operation: {a} * {b} = {result}")
    return result
```

### `divide(a: float, b: float) -> float`
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    result = a / b
    logger.info(f"Divide operation: {a} / {b} = {result}")
    return result
```

### `get_calculator_tools() -> List[Dict]`
Returns tool definitions in JSON schema format for Gemini:
```python
[
    {
        "type": "function",
        "name": "add",
        "description": "Add two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    # ... similar for subtract, multiply, divide
]
```

### `execute_tool(tool_name, tool_args) -> Union[float, str]`
Dispatcher that routes to the correct function:
```python
def execute_tool(tool_name: str, tool_args: Dict) -> Union[float, str]:
    if tool_name == "add":
        return add(tool_args["a"], tool_args["b"])
    elif tool_name == "subtract":
        return subtract(tool_args["a"], tool_args["b"])
    elif tool_name == "multiply":
        return multiply(tool_args["a"], tool_args["b"])
    elif tool_name == "divide":
        return divide(tool_args["a"], tool_args["b"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
```

---

## 4. Configuration: src/config.py (70 lines)

**Purpose**: Centralized configuration and logging setup.

**Key Class**: `Config`

**Key Methods**:

### `setup_logging()`
Configures dual output (file + console):
```python
@classmethod
def setup_logging(cls):
    logger = logging.getLogger("calculator_bot")
    
    # File handler
    file_handler = logging.FileHandler("calculator_bot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
```

### `validate()`
Validates required configuration:
```python
@classmethod
def validate(cls) -> bool:
    if not cls.GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Please set it in .env file or as an environment variable."
        )
    return True
```

**Configuration Variables**:
- `GOOGLE_API_KEY`: Required - API key from Google
- `MODEL_NAME`: Optional - Gemini model (default: gemini-2.5-flash)
- `LOG_LEVEL`: Optional - Logging verbosity (default: INFO)

---

## 5. Environment Configuration: .env.example

**Purpose**: Template for environment variables (copy to .env and populate).

```env
# Google Generative AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Model Configuration
MODEL_NAME=gemini-2.5-flash
LOG_LEVEL=INFO
```

---

## 6. Dependencies: requirements.txt

```
google-genai>=0.3.0
python-dotenv>=1.0.0
```

Only 2 dependencies for minimal footprint!

---

## Function Calling Architecture

### Tool Schema Format (JSON)
```json
{
  "type": "function",
  "name": "add",
  "description": "Add two numbers together",
  "parameters": {
    "type": "object",
    "properties": {
      "a": {"type": "number", "description": "First number"},
      "b": {"type": "number", "description": "Second number"}
    },
    "required": ["a", "b"]
  }
}
```

### Function Call Execution Flow
```
User Input
    ↓
CalculatorAgent.interact()
    ↓
Convert tools to Gemini format
    ↓
Call: client.models.generate_content(tools=[tool_schema])
    ↓
Gemini returns function call request
    ↓
Extract tool_name and tool_args from response
    ↓
execute_tool(tool_name, tool_args)
    ↓
Function executes and returns result
    ↓
Format and display to user
```

---

## Integration Example

**Complete interaction flow**:

```python
# User enters: "What is 15 plus 8?"

# Agent receives and processes:
agent = CalculatorAgent()
result = agent.interact("What is 15 plus 8?")

# Inside interact():
# 1. Create tool schema
tool_schema = self._get_tool_schema()

# 2. Send to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is 15 plus 8?",
    config=types.GenerateContentConfig(tools=[tool_schema])
)

# 3. Gemini returns function call
# response.function_calls[0]:
#   - name: "add"
#   - args: {"a": 15, "b": 8}

# 4. Execute tool
result = execute_tool("add", {"a": 15, "b": 8})  # returns 23.0

# 5. Return formatted response
# "I performed the following calculation(s): 1. Add operation result: 23.0"
```

---

## Key Design Patterns

### 1. Separation of Concerns
- **agent.py**: Orchestration and API interaction
- **calculator.py**: Tool implementations
- **config.py**: Configuration and logging
- **main.py**: Entry point

### 2. Tool Schema Generation
Tools are defined once, then converted to JSON schema for Gemini:
```python
def get_calculator_tools():
    # Returns list of tool definitions in JSON format
    
def _get_tool_schema():
    # Converts to Gemini types.Tool format
```

### 3. Tool Execution Dispatcher
```python
def execute_tool(tool_name, tool_args):
    # Routes to appropriate function based on name
```

### 4. Error Handling
- Validation at startup (API key check)
- Tool execution error catching
- Division by zero protection
- Graceful error messages

---

## Logging Output Example

```
2024-06-01 11:30:45,123 - calculator_bot - INFO - Calculator Agent initialized
2024-06-01 11:30:45,456 - calculator_bot - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide']
2024-06-01 11:30:46,789 - calculator_bot - INFO - Processing user input: What is 15 plus 8?
2024-06-01 11:30:47,012 - calculator_bot - INFO - Model requested 1 function call(s)
2024-06-01 11:30:47,234 - calculator_bot - INFO - Executing function: add with args: {'a': 15, 'b': 8}
2024-06-01 11:30:47,456 - calculator_bot - INFO - Add operation: 15 + 8 = 23.0
2024-06-01 11:30:47,678 - calculator_bot - INFO - Tool add executed successfully. Result: 23.0
```

---

## Adding a New Tool

To add a new calculator function (e.g., square root):

### Step 1: Add function to calculator.py
```python
import math

def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    result = math.sqrt(x)
    logger.info(f"Square root operation: sqrt({x}) = {result}")
    return result
```

### Step 2: Add tool schema
```python
def get_calculator_tools():
    tools = [
        # ... existing tools ...
        {
            "type": "function",
            "name": "sqrt",
            "description": "Calculate the square root of a number",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Number"}
                },
                "required": ["x"]
            }
        }
    ]
    return tools
```

### Step 3: Update dispatcher
```python
def execute_tool(tool_name, tool_args):
    # ... existing tools ...
    elif tool_name == "sqrt":
        return sqrt(tool_args["x"])
```

### Step 4: Export the function
In `src/tools/__init__.py`:
```python
from .calculator import sqrt

__all__ = [
    "add", "subtract", "multiply", "divide", "sqrt",
    ...
]
```

The new tool is immediately available to Gemini!

---

## Quick Reference

| File | Lines | Purpose |
|------|-------|---------|
| main.py | 46 | Entry point |
| src/agent.py | 185 | Agent with function calling |
| src/tools/calculator.py | 196 | Tool implementations |
| src/config.py | 70 | Configuration & logging |
| src/__init__.py | 5 | Package metadata |
| src/tools/__init__.py | 19 | Tool exports |

**Total Code**: 521 lines  
**Total Documentation**: 920 lines  
**Total Project**: 1,441 lines

---

## Summary

The calculator bot demonstrates a complete ADK 2.0 implementation with:
- Clean agent architecture
- Gemini function calling integration
- Modular tool definitions
- Production-ready error handling
- Comprehensive logging
- Easy extensibility

Each file has a clear responsibility, and the entire codebase is documented, typed, and production-ready.
