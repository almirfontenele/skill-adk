"""Base Research Agent using Google Generative AI."""

from typing import Any, Callable, Optional

import google.genai as genai
from google.genai import types

from src.config import get_client
from src.tools.core_tools import search_web, summarize_content


class ResearchAgent:
    """A research agent powered by Gemini 2.5 Flash with web search and summarization tools."""

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        system_prompt: Optional[str] = None,
        tools: Optional[list[Callable]] = None,
    ):
        """Initialize the Research Agent.

        Args:
            model: The Gemini model to use (default: gemini-2.5-flash)
            system_prompt: Optional system prompt to guide the agent behavior
            tools: Optional list of tool functions to make available to the agent
        """
        self.model = model
        self.client = get_client()

        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                "You are a helpful research assistant. "
                "Use the available tools to search the web and summarize content. "
                "Always cite your sources when providing information."
            )
        self.system_prompt = system_prompt

        # Default tools if none provided
        if tools is None:
            tools = [search_web, summarize_content]
        self.tools = tools

        self.conversation_history: list[dict[str, str]] = []

    def chat(self, user_prompt: str) -> str:
        """Send a message to the agent and get a response.

        The agent will automatically use available tools to search the web,
        summarize content, and provide comprehensive responses.

        Args:
            user_prompt: The user's question or request

        Returns:
            str: The agent's response

        Raises:
            ValueError: If API call fails or no API key is configured
        """
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_prompt})

            # Prepare the message with system prompt
            messages = []
            if self.system_prompt:
                messages.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(self.system_prompt)],
                    )
                )

            # Add conversation history
            for msg in self.conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                messages.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(msg["content"])],
                    )
                )

            # Call the model with tools
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=self.tools,
                    temperature=0.7,
                ),
            )

            # Extract response text
            response_text = response.text or ""

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )

            return response_text

        except Exception as e:
            error_msg = f"Error calling Gemini API: {str(e)}"
            raise ValueError(error_msg) from e

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt.

        Args:
            prompt: The new system prompt
        """
        self.system_prompt = prompt
