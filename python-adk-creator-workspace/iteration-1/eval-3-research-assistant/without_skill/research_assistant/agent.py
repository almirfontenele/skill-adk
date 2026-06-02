"""Research agent implementation using Google Generative AI SDK."""

from typing import Any, Optional

from google.genai import types
from google.genai import Client

from research_assistant.config import Config
from research_assistant.tools import get_tool_handlers, get_tool_definitions


class ResearchAgent:
    """Research agent that performs web searches and content summarization."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the research agent.

        Args:
            config: Application configuration (uses default if not provided)
        """
        self.config = config or Config()
        self.config.validate()

        # Initialize the Generative AI client
        self.client = Client(api_key=self.config.GOOGLE_API_KEY)

        # Get tool definitions and handlers
        self.tools = get_tool_definitions(self.config)
        self.tool_handlers = get_tool_handlers()

    def research(self, query: str, use_tools: bool = True) -> str:
        """Perform research on a query using available tools.

        Args:
            query: The research query
            use_tools: Whether to use tools (default: True)

        Returns:
            Research findings as a string
        """
        try:
            # Build the generation config
            config = types.GenerateContentConfig(
                temperature=self.config.TEMPERATURE,
                top_p=self.config.TOP_P,
                max_output_tokens=self.config.MAX_TOKENS,
            )

            # Add tools if enabled
            if use_tools:
                config.tools = [self.tools]

            # Generate initial response
            response = self.client.models.generate_content(
                model=self.config.MODEL,
                contents=query,
                config=config,
            )

            # Process function calls if present
            if use_tools and response.function_calls:
                return self._process_function_calls(
                    response, query, config
                )

            return response.text

        except Exception as e:
            return f"Error during research: {str(e)}"

    def _process_function_calls(
        self,
        response: types.GenerateContentResponse,
        user_message: str,
        config: types.GenerateContentConfig,
    ) -> str:
        """Process function calls from the model response.

        Args:
            response: The initial model response
            user_message: The original user query
            config: The generation config

        Returns:
            Final response after processing function calls
        """
        # Build conversation history
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)],
            ),
            response.candidates[0].content,
        ]

        # Process each function call
        for function_call in response.function_calls:
            tool_name = function_call.name
            tool_args = function_call.args

            # Execute the tool
            result = self._execute_tool(tool_name, tool_args)

            # Add function response to conversation
            function_response_part = types.Part.from_function_response(
                name=tool_name,
                response=result,
            )
            function_response_content = types.Content(
                role="tool",
                parts=[function_response_part],
            )
            contents.append(function_response_content)

        # Get final response from model
        final_response = self.client.models.generate_content(
            model=self.config.MODEL,
            contents=contents,
            config=config,
        )

        return final_response.text

    def _execute_tool(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool with given arguments.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        handler = self.tool_handlers.get(tool_name)

        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return handler(**tool_args)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def interactive_session(self) -> None:
        """Start an interactive research session."""
        print("\n" + "=" * 60)
        print("Research Assistant - Interactive Mode")
        print("=" * 60)
        print("Available tools: web_search, summarize_content, fetch_page")
        print("Type 'quit' to exit\n")

        while True:
            try:
                query = input("Research query: ").strip()

                if query.lower() == "quit":
                    print("Goodbye!")
                    break

                if not query:
                    continue

                print("\nProcessing...\n")
                result = self.research(query)
                print(f"Result:\n{result}\n")
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")
