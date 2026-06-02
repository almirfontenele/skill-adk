"""Entry point for the Weather Agent CLI."""

import sys
from weather_agent import WeatherAgent


def main() -> None:
    """Run the weather agent in an interactive REPL."""
    print("Weather Agent - powered by Gemini")
    print("Type your weather questions below. Type 'quit' or 'exit' to stop.\n")

    try:
        agent = WeatherAgent()
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            agent.reset()
            print("Conversation history cleared.\n")
            continue

        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
