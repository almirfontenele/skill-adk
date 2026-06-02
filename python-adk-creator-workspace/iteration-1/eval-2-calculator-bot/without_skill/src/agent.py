"""Main agent logic for the Calculator Bot"""

import logging
from typing import Optional, Dict, Any
import google.genai as genai
from google.genai import types

from src.config import Config
from src.tools import get_calculator_tools, execute_tool

logger = logging.getLogger("calculator_bot")


class CalculatorAgent:
    """Agent that uses Gemini to perform mathematical operations via function calling"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Calculator Agent.

        Args:
            api_key: Google API key. If not provided, uses GOOGLE_API_KEY from config.
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model_name = Config.MODEL_NAME

        # Initialize the Gemini client
        genai.configure(api_key=self.api_key)
        self.client = genai.Client()

        # Get available tools
        self.tools = get_calculator_tools()

        logger.info(f"Calculator Agent initialized with model: {self.model_name}")
        logger.info(f"Available tools: {[tool['name'] for tool in self.tools]}")

    def _get_tool_schema(self) -> types.Tool:
        """
        Convert tool definitions to Gemini Tool format.

        Returns:
            types.Tool object with function declarations
        """
        function_declarations = []

        for tool in self.tools:
            func_decl = types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters_json_schema=tool["parameters"]
            )
            function_declarations.append(func_decl)

        return types.Tool(function_declarations=function_declarations)

    def process_tool_call(
        self,
        tool_name: str,
        tool_args: Dict[str, Any]
    ) -> str:
        """
        Process a tool call made by the model.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool

        Returns:
            String representation of the result
        """
        try:
            result = execute_tool(tool_name, tool_args)
            logger.info(f"Tool {tool_name} executed successfully. Result: {result}")
            return str(result)
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def interact(self, user_input: str) -> str:
        """
        Send a message to the agent and get a response.

        This method handles function calling - it will call the appropriate
        calculator tool if needed and return the result to the user.

        Args:
            user_input: The user's question or request

        Returns:
            The agent's response with the calculation result
        """
        logger.info(f"Processing user input: {user_input}")

        try:
            # Create the tool schema for Gemini
            tool_schema = self._get_tool_schema()

            # Send the request to the model with tools available
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_input,
                config=types.GenerateContentConfig(tools=[tool_schema])
            )

            logger.info(f"Received response from model: {response}")

            # Check if the model made any function calls
            if response.function_calls:
                logger.info(f"Model requested {len(response.function_calls)} function call(s)")

                # Process each function call
                tool_results = []
                for function_call in response.function_calls:
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)

                    logger.info(f"Executing function: {tool_name} with args: {tool_args}")

                    # Execute the tool
                    result = self.process_tool_call(tool_name, tool_args)
                    tool_results.append({
                        "tool_name": tool_name,
                        "result": result
                    })

                # Format the response with tool results
                response_text = f"I performed the following calculation(s):\n\n"
                for i, tool_result in enumerate(tool_results, 1):
                    response_text += f"{i}. {tool_result['tool_name'].capitalize()} operation result: {tool_result['result']}\n"

                return response_text.strip()

            # If no function calls, return the text response
            elif response.text:
                logger.info(f"Model responded with text: {response.text}")
                return response.text
            else:
                logger.warning("Received empty response from model")
                return "I couldn't generate a response. Please try again."

        except Exception as e:
            error_msg = f"Error during interaction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"An error occurred: {str(e)}"

    def run_interactive(self) -> None:
        """
        Run the agent in interactive mode, accepting user input from stdin.
        """
        logger.info("Starting interactive mode")
        print("Calculator Bot - ADK 2.0")
        print("=" * 50)
        print("Ask me to perform math operations!")
        print("Examples:")
        print("  - What is 15 plus 8?")
        print("  - Multiply 42 by 7")
        print("  - Divide 100 by 4")
        print("  - Subtract 25 from 50")
        print("=" * 50)
        print("Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit"]:
                    logger.info("User requested exit")
                    print("Goodbye!")
                    break

                # Get the response from the agent
                response = self.interact(user_input)
                print(f"Agent: {response}\n")

            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")
                print(f"Error: {str(e)}\n")
