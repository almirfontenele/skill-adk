#!/usr/bin/env python3
"""
Main entry point for the Calculator Bot - ADK 2.0

This script initializes the Calculator Agent and runs it in interactive mode.
The agent uses Gemini's function calling capabilities to perform mathematical operations.

Usage:
    python main.py

Requirements:
    - GOOGLE_API_KEY environment variable must be set
    - Dependencies: google-genai, python-dotenv
"""

import sys
import logging

from src.config import Config
from src.agent import CalculatorAgent


def main():
    """Main function to run the Calculator Bot"""
    try:
        # Validate configuration
        Config.validate()

        # Initialize the agent
        agent = CalculatorAgent()

        # Run in interactive mode
        agent.run_interactive()

    except ValueError as e:
        logging.error(f"Configuration error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
