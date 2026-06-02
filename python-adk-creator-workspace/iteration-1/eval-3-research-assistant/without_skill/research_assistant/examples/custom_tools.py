"""Example of using custom tools with the research agent."""

from google.genai import types

from research_assistant.agent import ResearchAgent
from research_assistant.config import Config
from research_assistant.tools import (
    WebSearchTool,
    ContentSummarizerTool,
    FetchPageTool,
)


def main():
    """Demonstrate custom tool usage."""
    config = Config()

    # Initialize individual tools
    search_tool = WebSearchTool(config)
    summarizer_tool = ContentSummarizerTool(config)
    fetch_tool = FetchPageTool(config)

    print("\n" + "=" * 70)
    print("Web Search Tool Example")
    print("=" * 70)
    result = search_tool.search("machine learning frameworks")
    print(f"Search Query: 'machine learning frameworks'")
    print(f"Results: {result}\n")

    print("=" * 70)
    print("Content Summarizer Tool Example")
    print("=" * 70)
    sample_text = (
        "Artificial Intelligence has revolutionized many industries. "
        "Machine learning enables computers to learn from data. "
        "Deep learning uses neural networks for complex tasks. "
        "Natural language processing helps machines understand text. "
        "Computer vision enables machines to interpret images."
    )
    result = summarizer_tool.summarize(sample_text, length=30)
    print(f"Original Text ({result['original_length']} words):")
    print(f"{sample_text}\n")
    print(f"Summary ({result['summary_length']} words):")
    print(f"{result['summary']}\n")

    print("=" * 70)
    print("Page Fetcher Tool Example")
    print("=" * 70)
    result = fetch_tool.fetch("https://example.com")
    if not result.get("error"):
        print(f"URL: {result['url']}")
        print(f"Content Length: {result['length']} characters")
        print(f"Content (first 200 chars): {result['content'][:200]}...\n")
    else:
        print(f"Error: {result['error']}\n")


if __name__ == "__main__":
    main()
