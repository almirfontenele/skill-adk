"""Base Weather Agent implementation using Gemini API."""

from typing import Optional, Any
import os
from google import genai
from google.genai import types


class WeatherAgent:
    """
    An AI agent that answers questions about weather using Gemini API.

    The agent can understand natural language questions and use integrated
    tools to fetch current weather and forecast information.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        """
        Initialize the Weather Agent.

        Args:
            api_key: Google API key. If None, loads from GOOGLE_API_KEY env var.
            model: The Gemini model to use for inference.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY must be provided or set as environment variable"
            )

        self.model = model
        self.client = genai.Client(api_key=self.api_key)
        self.conversation_history = []

        # Define weather tools for the agent
        self.tools = self._setup_tools()

    def _setup_tools(self) -> list:
        """
        Set up the tools available to the agent.

        Returns:
            list: List of function declarations for weather operations.
        """
        from src.tools.core_tools import get_current_weather, get_weather_forecast

        return [get_current_weather, get_weather_forecast]

    def chat(self, prompt: str) -> str:
        """
        Send a message to the agent and get a weather-related response.

        The agent automatically uses available tools to answer questions
        about current weather conditions and forecasts.

        Args:
            prompt: The user's question or request about weather.

        Returns:
            str: The agent's response to the user's query.
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": prompt})

        # Prepare the conversation for Gemini
        messages = []
        for msg in self.conversation_history:
            messages.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(msg["content"])],
                )
            )

        # Create system instruction for the agent
        system_instruction = """You are a helpful weather assistant powered by Gemini.
Your role is to answer questions about weather, including:
- Current weather conditions in specific locations
- Weather forecasts for upcoming days
- General weather information and explanations

When users ask about weather, use the available tools to fetch real data.
Provide clear, friendly responses with relevant weather details."""

        try:
            # Call Gemini API with tool use enabled
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=self.tools,
                    system_instruction=system_instruction,
                ),
            )

            # Extract the response text
            response_text = response.text

            # Handle tool use if the model requests it
            if response.tool_calls:
                response_text = self._handle_tool_calls(
                    response.tool_calls, prompt
                )

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )

            return response_text

        except Exception as e:
            error_message = f"Error communicating with Gemini API: {str(e)}"
            self.conversation_history.append(
                {"role": "assistant", "content": error_message}
            )
            return error_message

    def _handle_tool_calls(self, tool_calls: list, original_prompt: str) -> str:
        """
        Execute tool calls requested by the model.

        Args:
            tool_calls: List of tool calls from the model.
            original_prompt: The original user prompt.

        Returns:
            str: The final response after executing tools.
        """
        from src.tools.core_tools import get_current_weather, get_weather_forecast

        tool_results = []
        for tool_call in tool_calls:
            try:
                if tool_call.name == "get_current_weather":
                    result = get_current_weather(**tool_call.args)
                    tool_results.append(
                        types.Part.from_function_response(
                            name=tool_call.name, response={"result": result}
                        )
                    )
                elif tool_call.name == "get_weather_forecast":
                    result = get_weather_forecast(**tool_call.args)
                    tool_results.append(
                        types.Part.from_function_response(
                            name=tool_call.name, response={"result": result}
                        )
                    )
            except Exception as e:
                tool_results.append(
                    types.Part.from_function_response(
                        name=tool_call.name,
                        response={"error": f"Tool execution failed: {str(e)}"},
                    )
                )

        # Send tool results back to the model for final response
        if tool_results:
            final_messages = self.conversation_history.copy()
            final_messages.append(
                {"role": "user", "content": "Please use the tool results above to answer my original question."}
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=final_messages,
                config=types.GenerateContentConfig(tools=self.tools),
            )
            return response.text

        return "I couldn't fetch the weather information you requested."

    def reset_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
