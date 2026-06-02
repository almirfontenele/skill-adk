"""Base agent implementation for Calculator Bot using Gemini API.

This module provides the core GeminiAgent class that leverages the Gemini API
for function calling and mathematical operations.
"""

from typing import Any, Callable, Optional, List
from src.config import get_client, MODEL_ID


class GeminiAgent:
    """
    A Gemini-powered agent that can execute mathematical operations.

    The agent uses Google's Generative AI API with automatic function calling
    to perform calculator operations and explain mathematical concepts.
    """

    def __init__(
        self,
        tools: Optional[List[Callable]] = None,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the GeminiAgent.

        Args:
            tools: List of callable functions that the agent can use
            system_prompt: Optional system prompt to guide the agent's behavior
        """
        self.client = get_client()
        self.model = MODEL_ID
        self.tools = tools or []
        self.system_prompt = system_prompt or (
            "You are a helpful math assistant powered by Gemini. "
            "You can perform calculations and explain mathematical concepts. "
            "Use the available calculator tools to perform arithmetic operations "
            "when the user asks for calculations."
        )
        self.conversation_history = []

    def add_tool(self, tool: Callable) -> None:
        """
        Add a tool (callable function) to the agent.

        Args:
            tool: A callable function that performs a specific operation
        """
        if callable(tool):
            self.tools.append(tool)
        else:
            raise ValueError(f"Tool must be callable, got {type(tool)}")

    def chat(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.

        This method handles automatic function calling when the model
        determines that a tool needs to be invoked.

        Args:
            user_message: The user's input message

        Returns:
            str: The agent's response
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        try:
            # Prepare the request with system prompt
            messages = self._prepare_messages()

            # Generate content with tools
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config={
                    "tools": self.tools if self.tools else None,
                    "temperature": 0.7,
                },
            )

            # Extract and process response
            response_text = response.text

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )

            return response_text

        except Exception as e:
            error_message = f"Error communicating with Gemini API: {str(e)}"
            print(error_message)
            raise

    def _prepare_messages(self) -> List[dict]:
        """
        Prepare messages for the API call with system prompt.

        Returns:
            List[dict]: Formatted messages for the API
        """
        messages = []

        # Add system prompt as first message
        if self.system_prompt:
            messages.append({"role": "user", "content": self.system_prompt})
            messages.append(
                {"role": "assistant", "content": "I understand. I'm ready to help!"}
            )

        # Add conversation history
        messages.extend(self.conversation_history)

        return messages

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[dict]:
        """
        Get the conversation history.

        Returns:
            List[dict]: The current conversation history
        """
        return self.conversation_history.copy()
