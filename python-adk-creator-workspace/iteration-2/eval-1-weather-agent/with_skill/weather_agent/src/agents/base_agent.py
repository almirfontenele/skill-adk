"""Generic GeminiAgent class for orchestrating Gemini models with tools."""

from google import genai
from google.genai import types
from src.config import get_api_key


class GeminiAgent:
    """A generic agent that uses Gemini with automatic function calling."""

    def __init__(
        self,
        tools: list,
        system_prompt: str = "",
        model: str = "gemini-2.5-flash",
    ):
        """
        Initialize the GeminiAgent.

        Args:
            tools: List of Python functions to register as tools.
            system_prompt: Optional system instruction for the agent.
            model: Gemini model ID to use.
        """
        self.client = genai.Client(api_key=get_api_key())
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self.history: list[types.Content] = []

    def chat(self, prompt: str) -> str:
        """
        Send a prompt to the agent and return the text response.

        Automatic function calling is used — the SDK executes registered tools
        automatically and returns the final text without any manual tool loop.

        Args:
            prompt: User message to send to the agent.

        Returns:
            The agent's final text response.
        """
        self.history.append(
            types.Content(role="user", parts=[types.Part.from_text(prompt)])
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.history,
                config=types.GenerateContentConfig(
                    tools=self.tools,
                    system_instruction=self.system_prompt or None,
                ),
            )
            reply = response.text
            self.history.append(
                types.Content(role="model", parts=[types.Part.from_text(reply)])
            )
            return reply
        except Exception as e:
            raise RuntimeError(f"Error communicating with Gemini API: {e}") from e

    def reset(self) -> None:
        """Clear conversation history."""
        self.history = []
