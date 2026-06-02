"""Calculator tools for mathematical operations"""

import logging
from typing import Dict, Any, List, Union

logger = logging.getLogger("calculator_bot")


def add(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    result = a + b
    logger.info(f"Add operation: {a} + {b} = {result}")
    return result


def subtract(a: float, b: float) -> float:
    """
    Subtract one number from another.

    Args:
        a: First number (minuend)
        b: Second number (subtrahend)

    Returns:
        The difference of a and b
    """
    result = a - b
    logger.info(f"Subtract operation: {a} - {b} = {result}")
    return result


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    result = a * b
    logger.info(f"Multiply operation: {a} * {b} = {result}")
    return result


def divide(a: float, b: float) -> float:
    """
    Divide one number by another.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        The quotient of a and b

    Raises:
        ValueError: If b is zero (division by zero)
    """
    if b == 0:
        logger.error(f"Division by zero attempted: {a} / {b}")
        raise ValueError("Division by zero is not allowed")
    result = a / b
    logger.info(f"Divide operation: {a} / {b} = {result}")
    return result


def get_calculator_tools() -> List[Dict[str, Any]]:
    """
    Get the list of calculator tools as tool definitions for Gemini.

    Returns:
        List of tool definitions in JSON schema format
    """
    tools = [
        {
            "type": "function",
            "name": "add",
            "description": "Add two numbers together. Use this when the user asks to add, sum, or perform addition.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to add"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to add"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "type": "function",
            "name": "subtract",
            "description": "Subtract one number from another. Use this when the user asks to subtract, take away, or perform subtraction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number (minuend)"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to subtract (subtrahend)"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "type": "function",
            "name": "multiply",
            "description": "Multiply two numbers together. Use this when the user asks to multiply, calculate the product, or perform multiplication.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number to multiply"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number to multiply"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "type": "function",
            "name": "divide",
            "description": "Divide one number by another. Use this when the user asks to divide, calculate the quotient, or perform division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The dividend (number being divided)"
                    },
                    "b": {
                        "type": "number",
                        "description": "The divisor (number to divide by)"
                    }
                },
                "required": ["a", "b"]
            }
        }
    ]
    return tools


def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> Union[float, str]:
    """
    Execute a calculator tool by name with the given arguments.

    Args:
        tool_name: Name of the tool to execute (add, subtract, multiply, divide)
        tool_args: Dictionary of arguments for the tool

    Returns:
        The result of the tool execution

    Raises:
        ValueError: If the tool name is not recognized
    """
    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

    try:
        if tool_name == "add":
            return add(tool_args["a"], tool_args["b"])
        elif tool_name == "subtract":
            return subtract(tool_args["a"], tool_args["b"])
        elif tool_name == "multiply":
            return multiply(tool_args["a"], tool_args["b"])
        elif tool_name == "divide":
            return divide(tool_args["a"], tool_args["b"])
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        raise
