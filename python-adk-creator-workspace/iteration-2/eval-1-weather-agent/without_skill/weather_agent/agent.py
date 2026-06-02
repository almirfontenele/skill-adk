"""WeatherAgent - A Gemini-powered conversational weather assistant."""

import os
from google import genai
from google.genai import types

from .tools import get_current_weather, get_weather_forecast

_SYSTEM_INSTRUCTION = """You are a helpful weather assistant powered by real-time weather data.
You can:
- Retrieve current weather conditions for any city in the world.
- Provide multi-day weather forecasts (up to 16 days).

When answering:
- Always use the provided tools to fetch accurate, live data.
- Interpret the data in a friendly, conversational way.
- Include relevant details such as temperature, conditions, precipitation, and wind.
- If asked for a forecast without specifying days, default to 7 days.
- Use metric units (Celsius, km/h) by default unless the user asks otherwise.
- If a location is ambiguous, ask for clarification.
"""


class WeatherAgent:
    """Conversational weather agent backed by Gemini with automatic function calling."""

    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None):
        """Initialize the WeatherAgent.

        Args:
            model: Gemini model ID to use.
            api_key: Google AI API key. Falls back to the GOOGLE_API_KEY env var.

        Raises:
            ValueError: If no API key is available.
        """
        resolved_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not resolved_key:
            raise ValueError(
                "A Google AI API key is required. "
                "Set the GOOGLE_API_KEY environment variable or pass api_key=."
            )

        self._client = genai.Client(api_key=resolved_key)
        self._model = model
        self._tools = [get_current_weather, get_weather_forecast]
        self._config = types.GenerateContentConfig(
            system_instruction=_SYSTEM_INSTRUCTION,
            tools=self._tools,
            temperature=0.2,
        )
        self._history: list[types.Content] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(self, message: str) -> str:
        """Send a message and receive a response, maintaining conversation history.

        Args:
            message: User message text.

        Returns:
            The assistant's response as a string.
        """
        chat_session = self._client.chats.create(
            model=self._model,
            config=self._config,
            history=self._history,
        )
        response = chat_session.send_message(message)
        # Persist updated history for the next turn
        self._history = chat_session.get_history()
        return response.text

    def ask(self, question: str) -> str:
        """Ask a one-shot weather question without maintaining conversation history.

        Args:
            question: The weather-related question.

        Returns:
            The assistant's answer as a string.
        """
        response = self._client.models.generate_content(
            model=self._model,
            contents=question,
            config=self._config,
        )
        return response.text

    def reset(self) -> None:
        """Clear the conversation history to start a fresh session."""
        self._history = []
