# Calculator Bot - Project Structure

## Overview

This is a production-ready Python project implementing an ADK 2.0 calculator bot using Google's Generative AI SDK. The bot leverages Gemini's function calling capabilities to autonomously perform mathematical operations based on natural language input.

## Complete Directory Tree

```
calculator_bot/
│
├── main.py                          # Entry point - runs the agent in interactive mode
├── requirements.txt                 # Project dependencies
├── .env.example                     # Template for environment variables
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── PROJECT_STRUCTURE.md             # This file - detailed structure documentation
│
└── src/                             # Source code package
    ├── __init__.py                  # Package initialization
    ├── config.py                    # Configuration management and logging setup
    ├── agent.py                     # Main agent logic with function calling
    │
    └── tools/                       # Calculator tool definitions
        ├── __init__.py              # Package initialization
        └── calculator.py            # Calculator functions and tool schemas
```

## File Descriptions

### Root Level

#### `main.py`
**Purpose**: Main entry point for the application

**Key Components**:
- Imports and validates configuration
- Initializes the CalculatorAgent
- Starts interactive mode
- Handles exceptions and system exits

**Usage**: `python main.py`

#### `requirements.txt`
**Purpose**: Python package dependencies

**Dependencies**:
- `google-genai>=0.3.0`: Google Generative AI SDK
- `python-dotenv>=1.0.0`: Environment variable management

#### `.env.example`
**Purpose**: Template for environment configuration

**Variables**:
- `GOOGLE_API_KEY`: Required API key from Google
- `MODEL_NAME`: Gemini model to use (default: gemini-2.5-flash)
- `LOG_LEVEL`: Logging verbosity (default: INFO)

#### `.gitignore`
**Purpose**: Git repository rules to exclude files from version control

**Excludes**:
- Environment files (.env, .env.local)
- Virtual environment directories
- Python cache and compiled files
- IDE configuration directories
- Test coverage reports
- Log files

#### `README.md`
**Purpose**: User-facing project documentation

**Includes**:
- Feature list
- Project structure overview
- Setup and installation instructions
- Usage examples
- Configuration details
- Development guidelines

#### `PROJECT_STRUCTURE.md`
**Purpose**: Detailed architectural documentation (this file)

### src/ Package

Main source code package containing agent logic and tools.

#### `src/__init__.py`
**Purpose**: Package initialization and metadata

**Exports**:
- Version information
- Author details
- Package description

#### `src/config.py`
**Purpose**: Centralized configuration management

**Key Classes**:
- `Config`: Central configuration class

**Key Features**:
- Loads environment variables from `.env` file
- Validates required API keys
- Configures logging (file + console output)
- Sets model name, timeouts, and retry parameters

**Key Methods**:
- `setup_logging()`: Initializes logging system
- `validate()`: Validates required configuration values

#### `src/agent.py`
**Purpose**: Main agent implementation with function calling

**Key Classes**:
- `CalculatorAgent`: Autonomous agent using Gemini

**Key Features**:
- Initializes Gemini client with API key
- Manages tool definitions and schemas
- Handles function calling lifecycle
- Processes tool results from model
- Provides interactive interface

**Key Methods**:
- `__init__(api_key)`: Initializes agent and client
- `_get_tool_schema()`: Converts tools to Gemini format
- `interact(user_input)`: Main interaction method with function calling
- `process_tool_call(tool_name, tool_args)`: Executes individual tools
- `run_interactive()`: Starts interactive prompt loop

**Function Calling Flow**:
1. User provides natural language input
2. Agent sends request to Gemini with available tools
3. Gemini analyzes request and calls appropriate tool (if needed)
4. Agent executes tool and returns result
5. Result is formatted and presented to user

### src/tools/ Package

Calculator tool implementations and schemas.

#### `src/tools/__init__.py`
**Purpose**: Package initialization and public API

**Exports**:
- `add`, `subtract`, `multiply`, `divide`: Tool functions
- `get_calculator_tools()`: Tool schema generator
- `execute_tool()`: Tool executor dispatcher

#### `src/tools/calculator.py`
**Purpose**: Calculator tool implementations and definitions

**Tool Functions**:

1. **`add(a: float, b: float) -> float`**
   - Description: Add two numbers
   - Logging: Logs operation and result
   - Returns: Sum

2. **`subtract(a: float, b: float) -> float`**
   - Description: Subtract two numbers
   - Logging: Logs operation and result
   - Returns: Difference

3. **`multiply(a: float, b: float) -> float`**
   - Description: Multiply two numbers
   - Logging: Logs operation and result
   - Returns: Product

4. **`divide(a: float, b: float) -> float`**
   - Description: Divide two numbers
   - Logging: Logs operation and result
   - Error Handling: Raises ValueError on division by zero
   - Returns: Quotient

**Utility Functions**:

- **`get_calculator_tools() -> List[Dict[str, Any]]`**
  - Returns tool definitions in JSON schema format
  - Each tool includes:
    - `type`: "function"
    - `name`: Tool identifier
    - `description`: Natural language description for Gemini
    - `parameters`: JSON schema defining input parameters
  - Used by agent to define available functions

- **`execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> Union[float, str]`**
  - Dispatcher function to execute tools by name
  - Validates tool name
  - Executes appropriate function with arguments
  - Returns result or error message
  - Logs all executions

## Architecture Patterns

### Configuration Management
- Centralized in `src/config.py`
- Environment variables loaded via dotenv
- Validation of required parameters at startup

### Logging
- Dual output: file (`calculator_bot.log`) and console
- Structured logging with timestamps
- Different log levels per handler

### Tool Definitions
- JSON schema compliant for Gemini compatibility
- Descriptive names and help text
- Type-safe parameter definitions

### Function Calling Loop
- Agent sends tools to Gemini model
- Model analyzes user input and calls appropriate tool
- Tool executes with provided arguments
- Results returned to user in natural language

## Development Workflow

### Adding New Calculator Functions

1. **Define function** in `src/tools/calculator.py`
   ```python
   def power(base: float, exponent: float) -> float:
       """Calculate base raised to exponent"""
       return base ** exponent
   ```

2. **Add tool schema** to `get_calculator_tools()`
   ```python
   {
       "type": "function",
       "name": "power",
       "description": "Raise a number to a power",
       "parameters": {
           "type": "object",
           "properties": {
               "base": {"type": "number", "description": "Base number"},
               "exponent": {"type": "number", "description": "Exponent"}
           },
           "required": ["base", "exponent"]
       }
   }
   ```

3. **Update dispatcher** in `execute_tool()`
   ```python
   elif tool_name == "power":
       return power(tool_args["base"], tool_args["exponent"])
   ```

4. **Update exports** in `src/tools/__init__.py`

### Testing
Run the interactive agent and test with various mathematical queries:
```bash
python main.py
```

Example test queries:
- "What is 15 plus 8?"
- "Multiply 42 by 7"
- "Divide 100 by 4"
- "Subtract 25 from 50"

## Dependencies

### google-genai
- Version: >= 0.3.0
- Purpose: Google Generative AI SDK for Gemini integration
- Usage: Client initialization, content generation, function calling

### python-dotenv
- Version: >= 1.0.0
- Purpose: Load environment variables from .env files
- Usage: Configuration loading

## Configuration Files

### .env (Not tracked in git)
```
GOOGLE_API_KEY=your_key_here
MODEL_NAME=gemini-2.5-flash
LOG_LEVEL=INFO
```

### .env.example (Tracked in git)
Template showing required and optional environment variables.

## Logging Output

Logs are written to `calculator_bot.log` with the following information:
- Timestamp
- Logger name (calculator_bot)
- Log level (DEBUG, INFO, WARNING, ERROR)
- Message content

Example log entries:
```
2024-01-15 10:30:45,123 - calculator_bot - INFO - Calculator Agent initialized with model: gemini-2.5-flash
2024-01-15 10:30:46,456 - calculator_bot - INFO - Processing user input: What is 15 plus 8?
2024-01-15 10:30:47,789 - calculator_bot - INFO - Executing function: add with args: {'a': 15, 'b': 8}
2024-01-15 10:30:48,012 - calculator_bot - INFO - Add operation: 15 + 8 = 23.0
```

## Error Handling

### Configuration Errors
- Missing GOOGLE_API_KEY: Raises ValueError with clear message
- Invalid configuration: Logged and reported to user

### Tool Execution Errors
- Division by zero: Caught and handled with informative error
- Invalid tool name: Raises ValueError
- Execution exceptions: Logged with full traceback

### Network Errors
- API failures: Caught and returned as user-friendly messages
- Connection timeouts: Handled with configured timeout

## Production Readiness

✅ **Complete**:
- Environment configuration management
- Comprehensive logging system
- Error handling and validation
- Type hints throughout codebase
- Docstrings on all functions and classes
- .gitignore for sensitive files
- README with setup instructions
- Modular architecture for extensibility

✅ **Extensible**:
- Easy to add new calculator functions
- Tool schema system for adding capabilities
- Configurable model selection
- Customizable logging levels

✅ **Professional Quality**:
- Follows Python best practices
- Clear separation of concerns
- Proper exception handling
- Comprehensive documentation
- Production-ready structure
