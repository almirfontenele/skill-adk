# Contributing to Weather Agent

Thank you for your interest in contributing to the Weather Agent project!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weather-agent.git
   cd weather-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

## Code Standards

- **Python Version**: 3.8+
- **Code Style**: Black (88 character line length)
- **Import Sorting**: isort
- **Linting**: flake8
- **Type Hints**: Encouraged (mypy compatible)

## Running Tests

```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

## Code Formatting

```bash
# Format code
black src/ main.py

# Sort imports
isort src/ main.py

# Lint code
flake8 src/ main.py
```

## Adding New Features

1. Create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature with tests

3. Ensure code passes all checks:
   ```bash
   black src/
   isort src/
   flake8 src/
   mypy src/
   pytest
   ```

4. Submit a pull request with a clear description

## Adding New Weather Tools

1. Add the tool function to `src/weather_agent/tools.py`
2. Add type hints and docstrings
3. Update the `get_all_tools()` method
4. Update `src/weather_agent/agent.py` to include it in tool definitions
5. Add tests in `tests/test_tools.py`
6. Update README.md documentation

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update CONTRIBUTING.md if needed

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new weather alerts tool
fix: Handle missing location parameter
docs: Update tool documentation
refactor: Simplify tool execution logic
test: Add tests for weather comparison
```

## Pull Request Process

1. Fork the repository
2. Create your feature branch
3. Make your changes with tests
4. Ensure all tests pass and code is properly formatted
5. Submit a PR with description of changes
6. Address any review feedback
7. Once approved, your PR will be merged

## Questions?

Open an issue to discuss ideas or report bugs!
