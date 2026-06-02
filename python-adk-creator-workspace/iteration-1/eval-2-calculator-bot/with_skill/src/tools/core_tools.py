"""Core calculator tools for mathematical operations.

This module contains the fundamental arithmetic operations used by the agent.
Each function is designed to be called by the Gemini API for automatic function calling.
"""

from typing import Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.

    Args:
        a: The first number
        b: The second number

    Returns:
        Union[int, float]: The sum of a and b

    Examples:
        >>> add(5, 3)
        8
        >>> add(2.5, 1.5)
        4.0
    """
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Subtract one number from another.

    Args:
        a: The minuend (number to subtract from)
        b: The subtrahend (number to subtract)

    Returns:
        Union[int, float]: The difference (a - b)

    Examples:
        >>> subtract(10, 4)
        6
        >>> subtract(7.5, 2.5)
        5.0
    """
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiply two numbers together.

    Args:
        a: The first factor
        b: The second factor

    Returns:
        Union[int, float]: The product of a and b

    Examples:
        >>> multiply(6, 7)
        42
        >>> multiply(2.5, 4)
        10.0
    """
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Divide one number by another.

    Args:
        a: The dividend (number to be divided)
        b: The divisor (number to divide by)

    Returns:
        Union[int, float]: The quotient (a / b)

    Raises:
        ValueError: If attempting to divide by zero

    Examples:
        >>> divide(20, 4)
        5.0
        >>> divide(15, 3)
        5.0
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
