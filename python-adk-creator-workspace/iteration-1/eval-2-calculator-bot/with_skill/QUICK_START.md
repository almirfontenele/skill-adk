# Calculator Bot - Quick Start Guide

## 30-Second Setup

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your Google API key
nano .env

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the bot
python main.py
```

## Verify Installation Works

After running `python main.py`, you should see:
```
============================================================
Calculator Bot - Powered by Gemini
============================================================

Agent initialized successfully with calculator tools!

Running example queries...
```

Then the bot will:
1. Answer pre-defined math questions
2. Enter interactive mode where you can ask your own questions

## Example Questions to Try

```
What is 25 plus 17?
Calculate 100 divided by 4
Multiply 12 by 8
What is 156 minus 49?
Add 5, 10, and 15 together
```

## Use as a Library

```python
from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide

# Create agent
agent = GeminiAgent(tools=[add, subtract, multiply, divide])

# Ask a question
response = agent.chat("What is 42 divided by 6?")
print(response)  # Output: "7.0"
```

## Project Files Reference

| File | Purpose |
|------|---------|
| `main.py` | Run this to start the bot |
| `src/agents/base_agent.py` | Core agent logic |
| `src/tools/core_tools.py` | Calculator functions |
| `src/config.py` | API configuration |
| `requirements.txt` | Install with: `pip install -r requirements.txt` |
| `README.md` | Full documentation |

## Common Issues

**"GOOGLE_API_KEY not found"**
- Did you create `.env` from `.env.example`?
- Did you add your actual API key?

**"google-genai not installed"**
- Run: `pip install -r requirements.txt`

**"ModuleNotFoundError"**
- Are you running from the project root?
- Is your virtual environment activated?

## Next: Customization

Edit `main.py` to change the system prompt:

```python
agent = GeminiAgent(
    tools=[add, subtract, multiply, divide],
    system_prompt="You are a strict mathematics tutor..."  # <-- Change this
)
```

## Adding New Math Functions

Edit `src/tools/core_tools.py` and add:

```python
def power(base, exponent):
    """Raise base to the power of exponent."""
    return base ** exponent
```

Then use it:

```python
from src.tools import power
agent.add_tool(power)
agent.chat("What is 2 to the power of 8?")
```

## Further Reading

- See `README.md` for complete documentation
- See `PROJECT_SUMMARY.md` for architecture overview
- See `PROJECT_TREE.txt` for detailed structure

---

**Ready to start?** Run: `python main.py`
