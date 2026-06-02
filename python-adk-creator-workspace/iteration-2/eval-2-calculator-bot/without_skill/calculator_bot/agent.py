"""Calculator bot agent using Google ADK 2.0."""

from google.adk.agents import Agent

from calculator_bot.tools import add, divide, multiply, subtract

root_agent = Agent(
    name="calculator_bot",
    model="gemini-2.0-flash",
    description="A helpful calculator bot that can perform basic math operations.",
    instruction=(
        "You are a friendly and helpful calculator assistant. "
        "You help users perform mathematical operations including addition, subtraction, "
        "multiplication, and division. "
        "When a user asks you to perform a calculation, use the appropriate tool. "
        "Always show the result clearly and offer to help with more calculations. "
        "If the user asks for division by zero, explain that it is mathematically undefined."
    ),
    tools=[add, subtract, multiply, divide],
)
