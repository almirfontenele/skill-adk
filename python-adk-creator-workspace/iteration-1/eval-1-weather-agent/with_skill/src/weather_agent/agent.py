"""Main Weather Agent implementation using Google Generative AI."""

from typing import Optional, Dict, Any, List
import logging
from google import genai
from google.genai import types
from .config import Config
from .tools import WeatherTools
from .models import AgentResponse

logger = logging.getLogger(__name__)


class WeatherAgent:
    """Weather Agent powered by Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Weather Agent.
        
        Args:
            api_key: Google API key (uses config if not provided)
            model: Model name (uses config if not provided)
        """
        Config.validate()
        
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model = model or Config.GEMINI_MODEL
        self.client = genai.Client(api_key=self.api_key)
        self.tools = WeatherTools()
        self.tool_calls_made: List[str] = []
        
        logger.info(f"Weather Agent initialized with model: {self.model}")
    
    def _execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Result from the tool
        """
        logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
        self.tool_calls_made.append(tool_name)
        
        if tool_name == "get_current_weather":
            return self.tools.get_current_weather(kwargs.get("location", ""))
        elif tool_name == "get_weather_forecast":
            return self.tools.get_weather_forecast(
                kwargs.get("location", ""),
                kwargs.get("days", 5)
            )
        elif tool_name == "compare_weather":
            return self.tools.compare_weather(
                kwargs.get("location1", ""),
                kwargs.get("location2", "")
            )
        elif tool_name == "get_weather_alerts":
            return self.tools.get_weather_alerts(kwargs.get("location", ""))
        else:
            logger.warning(f"Unknown tool: {tool_name}")
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}
    
    def _process_tool_calls(self, response) -> str:
        """
        Process any tool calls in the response.
        
        Args:
            response: Response from Gemini API
            
        Returns:
            String with tool execution results
        """
        tool_results = []
        
        if hasattr(response, 'function_calls') and response.function_calls:
            for call in response.function_calls:
                tool_name = call.name
                args = call.args if hasattr(call, 'args') else {}
                
                result = self._execute_tool(tool_name, **args)
                tool_results.append(f"Tool '{tool_name}' returned: {result}")
        
        return "\n".join(tool_results) if tool_results else ""
    
    def answer_question(self, query: str) -> AgentResponse:
        """
        Answer a question about weather using Gemini with function calling.
        
        Args:
            query: User's question about weather
            
        Returns:
            AgentResponse with answer and any weather data
        """
        logger.info(f"Processing query: {query}")
        self.tool_calls_made = []
        
        try:
            # Define tools for function calling
            tools = [
                {
                    "name": "get_current_weather",
                    "description": "Get current weather conditions for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name or location to get weather for"
                            }
                        },
                        "required": ["location"]
                    }
                },
                {
                    "name": "get_weather_forecast",
                    "description": "Get weather forecast for the next several days",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name or location"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days to forecast (1-14)",
                                "default": 5
                            }
                        },
                        "required": ["location"]
                    }
                },
                {
                    "name": "compare_weather",
                    "description": "Compare current weather between two locations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location1": {
                                "type": "string",
                                "description": "First location"
                            },
                            "location2": {
                                "type": "string",
                                "description": "Second location"
                            }
                        },
                        "required": ["location1", "location2"]
                    }
                },
                {
                    "name": "get_weather_alerts",
                    "description": "Get weather alerts for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name or location"
                            }
                        },
                        "required": ["location"]
                    }
                }
            ]
            
            # Make request to Gemini with tools
            config = types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=tools)],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode=types.FunctionCallingConfigMode.AUTO
                    )
                )
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=query,
                config=config
            )
            
            # Process the response
            response_text = ""
            if response.text:
                response_text = response.text
            
            # Handle function calls if present
            tool_results = self._process_tool_calls(response)
            if tool_results:
                response_text += f"\n\n{tool_results}"
            
            logger.info(f"Query processed successfully")
            
            return AgentResponse(
                query=query,
                response=response_text,
                tool_calls=self.tool_calls_made
            )
        
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return AgentResponse(
                query=query,
                response=f"Error: {str(e)}",
                tool_calls=self.tool_calls_made
            )
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Directly get current weather for a location.
        
        Args:
            location: City name or location
            
        Returns:
            Current weather data
        """
        return self.tools.get_current_weather(location)
    
    def get_forecast(self, location: str, days: int = 5) -> Dict[str, Any]:
        """
        Directly get weather forecast for a location.
        
        Args:
            location: City name or location
            days: Number of days for forecast
            
        Returns:
            Weather forecast data
        """
        return self.tools.get_weather_forecast(location, days)
