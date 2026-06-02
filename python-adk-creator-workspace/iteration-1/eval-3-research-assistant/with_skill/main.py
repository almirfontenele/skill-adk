#!/usr/bin/env python3
"""Main entry point for the Research Assistant."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.agents import ResearchAgent
from src.config import get_api_key


def main():
    """Run the research assistant in interactive mode."""
    print("=" * 60)
    print("Research Assistant - Powered by Gemini 2.5 Flash")
    print("=" * 60)
    print()
    print("This assistant can search the web and summarize content.")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    try:
        # Verify API key is configured
        get_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease configure your Google API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key to the GOOGLE_API_KEY field")
        print("3. Run this script again")
        sys.exit(1)

    # Initialize the research agent
    agent = ResearchAgent(
        system_prompt=(
            "You are a helpful research assistant with access to web search "
            "and content summarization tools. "
            "When users ask questions, use these tools to find and summarize information. "
            "Always cite your sources and provide accurate, helpful responses."
        )
    )

    print("Research Agent initialized successfully!\n")

    # Interactive chat loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit"]:
                print("\nThank you for using the Research Assistant. Goodbye!")
                break

            print("\nAssistant: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except ValueError as e:
            print(f"\nError: {e}")
            print("Please check your configuration and try again.\n")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again.\n")


def demo_mode():
    """Run the assistant with predefined demo queries."""
    print("=" * 60)
    print("Research Assistant - Demo Mode")
    print("=" * 60)
    print()

    try:
        get_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    agent = ResearchAgent()

    demo_queries = [
        "What are the latest developments in artificial intelligence?",
        "Can you summarize the key points about machine learning?",
    ]

    for query in demo_queries:
        print(f"User: {query}")
        response = agent.chat(query)
        print(f"Assistant: {response}")
        print()


if __name__ == "__main__":
    # Check for --demo flag
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        main()
