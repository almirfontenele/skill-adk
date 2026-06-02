"""Main entry point for the research assistant."""

import sys
from pathlib import Path

from research_assistant.agent import ResearchAgent
from research_assistant.config import get_config


def main(query: str = "", interactive: bool = False) -> None:
    """Run the research assistant.

    Args:
        query: Optional query to process in non-interactive mode
        interactive: Whether to run in interactive mode
    """
    try:
        # Load configuration
        config = get_config("development")

        # Initialize agent
        agent = ResearchAgent(config)

        if interactive:
            agent.interactive_session()
        elif query:
            print(f"\nResearching: {query}\n")
            result = agent.research(query)
            print(f"Result:\n{result}\n")
        else:
            print("Usage: python -m research_assistant.main [--interactive] [query]")
            print("\nOptions:")
            print("  --interactive  : Start interactive mode")
            print("  query          : Query to research")

    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        main(interactive=True)
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        main(query=query)
    else:
        main(interactive=True)
