# Calculator Bot

A intelligent math assistant powered by Google's Gemini API (ADK 2.0). This bot helps users perform arithmetic operations including addition, subtraction, multiplication, and division using natural language.

## Features

- **Natural Language Math** - Ask questions in plain English and get calculated results
- **Automatic Function Calling** - The Gemini API automatically calls the appropriate calculator functions
- **Arithmetic Operations** - Full support for add, subtract, multiply, and divide
- **Conversation History** - Maintains context across multiple interactions
- **Error Handling** - Graceful handling of division by zero and invalid inputs
- **Extensible Architecture** - Easy to add new tools and capabilities

## Project Structure

```
calculator_bot/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── base_agent.py          # GeminiAgent class with function calling
│   ├── tools/
│   │   ├── __init__.py
│   │   └── core_tools.py          # Calculator functions (add, subtract, multiply, divide)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── types.py               # Data type definitions
│   ├── __init__.py
│   └── config.py                  # Environment and API setup
├── main.py                        # Entry point with example usage
├── requirements.txt               # Python dependencies
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API key (get one from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone or copy the project** to your local machine

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

### Running the Bot

**Run the example script with predefined queries**:
```bash
python main.py
```

This will:
1. Initialize the calculator bot with all arithmetic tools
2. Run through example queries to demonstrate functionality
3. Enter interactive mode where you can ask your own math questions

**Example interactions**:
```
You: What is 25 plus 17?
Bot: The answer is 42. 25 + 17 = 42

You: Calculate 100 divided by 4
Bot: The result is 25. 100 ÷ 4 = 25

You: Multiply 12 by 8 and then subtract 10 from the result
Bot: First, 12 × 8 = 96. Then, 96 - 10 = 86. So the final answer is 86.
```

## Usage as a Library

You can also use the Calculator Bot in your own Python code:

```python
from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide

# Initialize the agent
agent = GeminiAgent(tools=[add, subtract, multiply, divide])

# Ask a question
response = agent.chat("What is 42 divided by 6?")
print(response)  # "7.0"
```

## Adding New Tools

To extend the calculator with additional operations:

1. **Add a new function** to `src/tools/core_tools.py`:
   ```python
   def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
       """Raise a number to a power."""
       return base ** exponent
   ```

2. **Import and register** the new tool:
   ```python
   from src.tools import add, subtract, multiply, divide, power

   agent = GeminiAgent(tools=[add, subtract, multiply, divide, power])
   ```

## API Reference

### GeminiAgent

Main agent class for interacting with Gemini API.

**Constructor**:
```python
GeminiAgent(
    tools: Optional[List[Callable]] = None,
    system_prompt: Optional[str] = None
)
```

**Methods**:
- `chat(user_message: str) -> str` - Send a message and get a response
- `add_tool(tool: Callable) -> None` - Add a tool to the agent
- `clear_history() -> None` - Clear conversation history
- `get_history() -> List[dict]` - Get conversation history

### Calculator Tools

- `add(a, b)` - Returns the sum of two numbers
- `subtract(a, b)` - Returns the difference (a - b)
- `multiply(a, b)` - Returns the product of two numbers
- `divide(a, b)` - Returns the quotient (a / b), raises ValueError if b is 0

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure you've created a `.env` file from `.env.example`
- Verify your API key is correctly set in the `.env` file
- Check for any whitespace issues in the key

### "google-genai not installed"
```bash
pip install -r requirements.txt
```

### "Module not found" errors
- Make sure you're running the script from the project root directory
- Verify the virtual environment is activated: `source venv/bin/activate`

### Model returns unexpected results
- The model behavior can vary; try rephrasing your question
- Check that your Google API key has access to the Gemini API
- Ensure you have sufficient API quota

## Model Information

- **Model**: Gemini 2.5 Flash
- **API**: Google Generative AI SDK (`google-genai`)
- **Automatic Function Calling**: Enabled by default

## Future Enhancements

Potential improvements for future versions:

- [ ] Add more advanced math functions (power, square root, modulo, etc.)
- [ ] Support for variables and multi-step equations
- [ ] Mathematical expression parsing and evaluation
- [ ] Structured output using Pydantic models
- [ ] Conversation memory with chat history management
- [ ] Unit tests and CI/CD integration
- [ ] REST API wrapper for the agent
- [ ] Async/await support for concurrent requests

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the [Google AI Python SDK documentation](https://github.com/googleapis/python-genai)
3. Visit [Google AI Studio](https://aistudio.google.com/) for API testing

## Acknowledgments

- Built with Google's Generative AI SDK (ADK 2.0)
- Powered by the Gemini API
