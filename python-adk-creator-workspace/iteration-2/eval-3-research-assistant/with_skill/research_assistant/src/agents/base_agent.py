"""Generic GeminiAgent using Google Generative AI SDK with automatic function calling."""

from google import genai
from google.genai import types
from src.config import get_api_key


class GeminiAgent:
    """A generic agent that uses Gemini with automatic function calling.

    This class is a pure orchestration shell — it has no knowledge of any
    specific domain. Tools are passed in at instantiation time.
    """

    def __init__(
        self,
        tools: list,
        system_prompt: str = "",
        model: str = "gemini-2.5-flash",
    ):
        """Initialize the agent with a list of tool functions.

        Args:
            tools: List of plain Python functions to register as tools.
            system_prompt: Optional system instruction for the model.
            model: Gemini model ID to use.
        """
        self.client = genai.Client(api_key=get_api_key())
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self.history: list[types.Content] = []

    def chat(self, prompt: str) -> str:
        """Send a prompt to Gemini and return the final text response.

        Automatic function calling is used — the SDK executes registered tool
        functions transparently and returns the final answer.

        Args:
            prompt: User message to send.

        Returns:
            Final text response after all tool calls have completed.
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
            error_msg = f"Error communicating with Gemini: {e}"
            return error_msg

    def reset(self) -> None:
        """Clear conversation history."""
        self.history = []
