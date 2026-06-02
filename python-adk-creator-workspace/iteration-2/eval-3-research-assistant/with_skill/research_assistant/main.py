"""Entry point for the research_assistant agent.

Demonstrates how to initialize the GeminiAgent with research tools
and interact with it via a simple chat loop.
"""

from src.agents.base_agent import GeminiAgent
from src.tools.core_tools import search_web, summarize_content, get_page_content

SYSTEM_PROMPT = """You are a helpful research assistant. You can search the web,
fetch page content, and summarize information to help users find answers.
Always cite your sources when possible and provide clear, concise responses."""


def main() -> None:
    """Run a demo conversation with the research assistant."""
    agent = GeminiAgent(
        tools=[search_web, summarize_content, get_page_content],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Research Assistant is ready. Type 'quit' to exit or 'reset' to clear history.\n")

    demo_queries = [
        "What is the latest news about artificial intelligence?",
        "Can you summarize what you found?",
    ]

    for query in demo_queries:
        print(f"You: {query}")
        response = agent.chat(query)
        print(f"Assistant: {response}\n")

    # Interactive loop
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            agent.reset()
            print("Conversation history cleared.\n")
            continue
        response = agent.chat(user_input)
        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    main()
