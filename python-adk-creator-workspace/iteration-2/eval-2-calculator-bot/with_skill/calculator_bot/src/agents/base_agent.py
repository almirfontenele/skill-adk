from google import genai
from google.genai import types
from src.config import get_api_key


class GeminiAgent:
    """Generic Gemini agent that supports automatic function calling with any set of tools."""

    def __init__(
        self,
        tools: list,
        system_prompt: str = "",
        model: str = "gemini-2.5-flash",
    ) -> None:
        self.client = genai.Client(api_key=get_api_key())
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self.history: list[types.Content] = []

    def chat(self, prompt: str) -> str:
        """Send a prompt to Gemini using automatic function calling and return the final text response."""
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
