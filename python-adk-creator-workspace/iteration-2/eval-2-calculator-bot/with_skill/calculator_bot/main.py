from src.agents import GeminiAgent
from src.tools import add, subtract, multiply, divide

SYSTEM_PROMPT = (
    "You are calculator_bot, a helpful math assistant. "
    "Use the provided tools to perform arithmetic operations accurately. "
    "Always show the result clearly to the user."
)

def main() -> None:
    """Run the calculator_bot demo."""
    agent = GeminiAgent(
        tools=[add, subtract, multiply, divide],
        system_prompt=SYSTEM_PROMPT,
    )

    print("calculator_bot is ready! Type 'quit' to exit or 'reset' to clear history.\n")

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

        try:
            response = agent.chat(user_input)
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
