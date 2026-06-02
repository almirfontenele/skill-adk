"""Basic research example."""

from research_assistant.agent import ResearchAgent
from research_assistant.config import Config


def main():
    """Run basic research example."""
    # Initialize with default config
    agent = ResearchAgent()

    # Example queries
    queries = [
        "What are the latest developments in artificial intelligence?",
        "Summarize the benefits of renewable energy sources",
        "What is the current state of quantum computing?",
    ]

    for query in queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        print("=" * 70)

        result = agent.research(query)
        print(f"Result:\n{result}")


if __name__ == "__main__":
    main()
