"""Main entry point for the Calculator Bot.

This script demonstrates how to use the GeminiAgent with calculator tools
to perform mathematical operations and answer math-related questions.
"""

import sys
from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide


def main():
    """Run the calculator bot with example queries."""

    print("=" * 60)
    print("Calculator Bot - Powered by Gemini")
    print("=" * 60)
    print()

    try:
        # Initialize the agent with calculator tools
        agent = GeminiAgent(
            tools=[add, subtract, multiply, divide],
            system_prompt=(
                "You are a helpful math assistant. "
                "You can perform arithmetic operations (add, subtract, multiply, divide). "
                "When the user asks for a calculation, use the available tools to compute the result. "
                "Always explain your work clearly."
            ),
        )

        print("Agent initialized successfully with calculator tools!")
        print()

        # Example questions to demonstrate the calculator bot
        example_queries = [
            "What is 25 plus 17?",
            "Calculate 100 divided by 4",
            "Multiply 12 by 8 and then subtract 10 from the result",
            "What is 156 minus 49?",
        ]

        print("Running example queries...")
        print("-" * 60)
        print()

        for i, query in enumerate(example_queries, 1):
            print(f"Query {i}: {query}")
            print("-" * 40)

            try:
                response = agent.chat(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {str(e)}")

            print()

        # Interactive mode
        print("=" * 60)
        print("Interactive Mode - Enter your math questions")
        print("(Type 'exit' or 'quit' to end)")
        print("=" * 60)
        print()

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                response = agent.chat(user_input)
                print(f"Bot: {response}")
                print()

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                print()

    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        print()
        print("Please ensure:")
        print("1. You have created a .env file from .env.example")
        print("2. Your GOOGLE_API_KEY is set in the .env file")
        print()
        print("Steps to set up:")
        print("  1. cp .env.example .env")
        print("  2. Edit .env and add your Google API key")
        print("  3. Run: python main.py")
        sys.exit(1)
    except ImportError as e:
        print(f"Import Error: {str(e)}")
        print()
        print("Please install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
