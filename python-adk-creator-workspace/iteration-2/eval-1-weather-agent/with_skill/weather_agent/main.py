"""Entry point for the weather_agent project.

Demonstrates how to initialize and use the GeminiAgent with weather tools.
Run from the project root: python main.py
"""

from src.agents.base_agent import GeminiAgent
from src.tools.core_tools import get_current_weather, get_weather_forecast

SYSTEM_PROMPT = (
    "You are a helpful weather assistant. Use the available tools to look up "
    "current weather conditions and forecasts for any city the user asks about. "
    "Always provide clear, friendly summaries of the weather data."
)


def main() -> None:
    agent = GeminiAgent(
        tools=[get_current_weather, get_weather_forecast],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Weather Agent is ready. Type 'quit' or 'exit' to stop.\n")

    demo_questions = [
        "What is the current weather in London?",
        "Give me a 3-day forecast for Tokyo.",
    ]

    for question in demo_questions:
        print(f"User: {question}")
        response = agent.chat(question)
        print(f"Agent: {response}\n")

    # Interactive loop
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", ""):
            print("Goodbye!")
            break
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
