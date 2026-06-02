# Research Assistant - Directory Structure

## Complete Project Layout

```
research_assistant/
│
├── src/
│   ├── __init__.py
│   │   └── Package initialization and version info
│   │
│   ├── config.py (48 lines)
│   │   ├── load_environment()
│   │   ├── get_api_key()
│   │   └── get_client()
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   │   └── Exports ResearchAgent class
│   │   │
│   │   └── base_agent.py (85 lines)
│   │       ├── ResearchAgent class
│   │       ├── chat(prompt) → Response
│   │       ├── clear_history() → None
│   │       └── set_system_prompt(prompt) → None
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   │   └── Exports search_web, summarize_content
│   │   │
│   │   └── core_tools.py (230 lines)
│   │       ├── search_web(query, max_results) → str
│   │       ├── summarize_content(content, max_length) → str
│   │       └── _simulate_search_results() → str
│   │
│   └── schemas/
│       ├── __init__.py
│       │   └── Package marker
│       │
│       └── types.py (25 lines)
│           ├── SearchQuery (Pydantic model)
│           ├── SummarySummary (Pydantic model)
│           └── SearchResult (Pydantic model)
│
├── main.py (110 lines)
│   ├── main() - Interactive chat mode
│   ├── demo_mode() - Demo with predefined queries
│   └── Entry point with argument parsing
│
├── requirements.txt (4 dependencies)
│   ├── google-genai==0.1.0
│   ├── pydantic>=2.0
│   ├── python-dotenv>=1.0.0
│   └── requests>=2.31.0
│
├── .env.example
│   └── GOOGLE_API_KEY=your-api-key-here
│
├── .gitignore
│   ├── .env (private)
│   ├── __pycache__ (compiled)
│   ├── venv/ (virtual environment)
│   └── Standard Python ignores
│
├── README.md
│   ├── Features overview
│   ├── Setup instructions
│   ├── Usage examples
│   ├── API reference
│   ├── Troubleshooting guide
│   └── Production deployment notes
│
├── PROJECT_OVERVIEW.md (This document)
│   ├── Architecture diagrams
│   ├── Module breakdown
│   ├── Data flow
│   ├── Technology stack
│   └── Enhancement roadmap
│
└── DIRECTORY_STRUCTURE.md
    └── File listing and description
```

## File Descriptions

### Core Application Files

#### `main.py` (110 lines)
**Purpose**: Entry point for the application

**Functions**:
- `main()`: Interactive chat loop
  - Validates API key
  - Initializes ResearchAgent
  - Reads user input
  - Displays agent responses
  - Handles exit commands

- `demo_mode()`: Runs predefined queries
  - Used with `--demo` flag
  - Useful for testing without manual input

**Usage**:
```bash
python main.py              # Interactive mode
python main.py --demo       # Demo mode
```

#### `src/config.py` (48 lines)
**Purpose**: Configuration and API setup

**Functions**:
- `load_environment()`: Loads .env file
- `get_api_key()`: Gets API key with validation
- `get_client()`: Returns authenticated Gemini client

**Key Features**:
- Automatic .env detection
- Clear error messages
- Type hints throughout

#### `src/agents/base_agent.py` (85 lines)
**Purpose**: Core agent implementation

**Class: ResearchAgent**
```python
ResearchAgent(
    model: str = "gemini-2.5-flash",
    system_prompt: Optional[str] = None,
    tools: Optional[list[Callable]] = None
)
```

**Key Methods**:
- `chat(user_prompt: str) -> str`: Send message, get response
- `clear_history() -> None`: Reset conversation
- `set_system_prompt(prompt: str) -> None`: Update behavior

**Features**:
- Automatic function calling
- Conversation history management
- Error handling with clear messages

#### `src/tools/core_tools.py` (230 lines)
**Purpose**: Tool implementations

**Tools Provided**:

1. **search_web(query: str, max_results: int = 5) -> str**
   - Searches web for information
   - Returns formatted results
   - Configurable result count
   - Currently simulated (can integrate real API)

2. **summarize_content(content: str, max_length: int = 200) -> str**
   - Summarizes text content
   - Preserves key information
   - Handles edge cases
   - Truncates gracefully

3. **_simulate_search_results(query: str, num_results: int) -> str**
   - Helper function for demo results
   - Can be replaced with real API

#### `src/schemas/types.py` (25 lines)
**Purpose**: Data validation models

**Models**:
- `SearchQuery`: Search request validation
- `SummarySummary`: Summary request validation
- `SearchResult`: Individual result structure

**Benefits**:
- Type safety
- IDE autocompletion
- Automatic validation
- Documentation

### Configuration Files

#### `requirements.txt`
**Purpose**: Python dependencies

```
google-genai==0.1.0        # Google AI SDK
pydantic>=2.0              # Data validation
python-dotenv>=1.0.0       # Env management
requests>=2.31.0           # HTTP library
```

#### `.env.example`
**Purpose**: Environment variable template

**Contents**:
```
GOOGLE_API_KEY=your-api-key-here
```

**Usage**:
1. Copy to `.env`: `cp .env.example .env`
2. Add your actual API key
3. Never commit `.env` to version control

#### `.gitignore`
**Purpose**: Prevent committing sensitive files

**Ignores**:
- `.env` (API keys)
- `__pycache__/` (compiled Python)
- `venv/` (virtual environment)
- `.vscode/`, `.idea/` (IDE configs)
- `*.pyc`, `*.pyo` (compiled files)

### Documentation Files

#### `README.md`
**Purpose**: User-facing documentation

**Sections**:
- Features overview
- Project structure
- Getting started (step-by-step)
- Usage examples
- Adding custom tools
- Advanced configuration
- Troubleshooting
- Production deployment

#### `PROJECT_OVERVIEW.md`
**Purpose**: Technical architecture documentation

**Sections**:
- Executive summary
- Architecture diagrams
- Module breakdown
- Data flow
- Technology stack
- Setup instructions
- Usage patterns
- Extension points
- Deployment options
- Testing strategy
- Troubleshooting
- Future enhancements
- Project statistics

#### `DIRECTORY_STRUCTURE.md`
**Purpose**: File organization and descriptions

**Contents**:
- Complete project tree
- File descriptions
- Function listings
- Usage information

## Package Organization

### `src/` Package
Root package for application logic.

**Structure**:
```python
from src.agents import ResearchAgent
from src.tools import search_web, summarize_content
from src.config import get_client
```

### `src.agents` Module
Contains agent implementations.

```python
from src.agents import ResearchAgent
agent = ResearchAgent()
```

### `src.tools` Module
Contains tool functions.

```python
from src.tools import search_web, summarize_content
```

### `src.schemas` Module
Contains Pydantic models.

```python
from src.schemas.types import SearchQuery, SearchResult
```

## Import Patterns

### Pattern 1: Direct Import
```python
from src.agents import ResearchAgent
from src.tools import search_web
```

### Pattern 2: Module Import
```python
import src.agents
agent = src.agents.ResearchAgent()
```

### Pattern 3: Relative Import (within package)
```python
# In src/agents/base_agent.py
from src.config import get_client
```

## File Sizes

| File | Lines | Purpose |
|------|-------|---------|
| main.py | 110 | Entry point |
| base_agent.py | 85 | Agent class |
| core_tools.py | 230 | Tool implementations |
| config.py | 48 | Configuration |
| types.py | 25 | Data models |
| __init__.py files | 10 | Package markers |
| .env.example | 1 | Config template |
| .gitignore | 25 | Git ignore rules |
| README.md | 350+ | User documentation |
| PROJECT_OVERVIEW.md | 400+ | Architecture docs |

**Total**: ~1,300+ lines

## Code Organization Principles

### 1. Separation of Concerns
- **config.py**: API setup only
- **agents/**: Agent logic
- **tools/**: Tool implementations
- **schemas/**: Data models
- **main.py**: User interface

### 2. Type Safety
- All functions have type hints
- Pydantic models for validation
- Clear return types

### 3. Error Handling
- Try/except in external calls
- Clear error messages
- Graceful degradation

### 4. Documentation
- Module-level docstrings
- Function docstrings
- Inline comments for complex logic
- Clear variable names

### 5. Extensibility
- Tools are simple functions
- Easy to add new tools
- Easy to subclass agents
- Config is centralized

## Module Dependencies

```
main.py
├── src.agents.ResearchAgent
├── src.config.get_api_key
└── src (package)

base_agent.py
├── google.genai
├── src.config
└── src.tools (for defaults)

core_tools.py
└── requests, re (standard library)

config.py
├── dotenv
└── google.genai

types.py
└── pydantic
```

## Running the Project

### Development
```bash
# From project root
python main.py
```

### Testing
```bash
python -m pytest
```

### Production
```bash
docker build -t research-assistant .
docker run -e GOOGLE_API_KEY=... research-assistant
```

## Next Steps After Setup

1. **Configure API Key**
   - Copy `.env.example` to `.env`
   - Add Google API key

2. **Install Dependencies**
   - Run `pip install -r requirements.txt`

3. **Run Application**
   - Execute `python main.py`

4. **Extend with Custom Tools**
   - Add functions to `src/tools/core_tools.py`

5. **Customize Agent Behavior**
   - Modify system prompt in main.py
   - Add domain-specific tools

6. **Deploy to Production**
   - Use Docker or cloud platform
   - Add logging and monitoring
   - Implement rate limiting

---

Generated: 2026-06-01
Project: research_assistant v0.1.0
