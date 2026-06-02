# Calculator Bot - ADK 2.0

A production-ready Python project using Google's Generative AI SDK (ADK 2.0) with Gemini agents and function calling to perform mathematical operations.

## Features

- **Agent-based Architecture**: Uses Google's Generative AI SDK with autonomous agents
- **Calculator Tools**: Add, subtract, multiply, and divide operations
- **Function Calling**: Gemini automatically invokes the right tool for calculations
- **Structured Outputs**: Type-safe tool definitions and responses
- **Production Ready**: Includes environment config, logging, and error handling

## Project Structure

```
calculator_bot/
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Main agent logic
│   ├── tools/
│   │   ├── __init__.py
│   │   └── calculator.py        # Calculator tool definitions
│   └── config.py                # Configuration management
├── main.py                       # Entry point
├── requirements.txt              # Project dependencies
├── .env.example                  # Environment variables template
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+
- Google API key for Gemini models

### Installation

1. Clone or extract the project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

## Usage

Run the calculator bot:

```bash
python main.py
```

Example interactions:
- "What is 15 plus 8?"
- "Multiply 42 by 7"
- "Divide 100 by 4"
- "Subtract 25 from 50"

## How It Works

1. **Agent Initialization**: The agent is configured with calculator tools
2. **Tool Definition**: Mathematical operations are defined as tools the model can invoke
3. **Function Calling**: When you ask a question, Gemini analyzes it and calls the appropriate tool
4. **Result Return**: The tool executes and returns the result to the user

## Configuration

Edit `src/config.py` to customize:
- Model selection (default: gemini-2.5-flash)
- Tool definitions and descriptions
- Logging levels
- System prompts

## Logging

Logs are written to `calculator_bot.log` with detailed information about:
- Agent interactions
- Tool calls and results
- Errors and exceptions

## Error Handling

The bot includes comprehensive error handling for:
- API failures
- Invalid tool calls
- Network issues
- Malformed responses

## Development

### Adding New Tools

1. Define a new function in `src/tools/calculator.py`
2. Add its JSON schema to the tools list in `src/agent.py`
3. Update the tool execution logic to handle the new tool
4. Test with example prompts

### Testing

Run with various mathematical questions to test functionality:
```bash
python main.py
```

## Dependencies

- `google-genai`: Google Generative AI SDK
- `python-dotenv`: Environment variable management

## License

MIT

## Support

For issues or questions about the Google Generative AI SDK, visit:
https://github.com/googleapis/python-genai
