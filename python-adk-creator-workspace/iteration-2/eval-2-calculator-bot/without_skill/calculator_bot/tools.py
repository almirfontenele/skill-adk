"""Math tools for the calculator bot."""


def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: The number to subtract from.
        b: The number to subtract.

    Returns:
        The result of a minus b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product of a and b.
    """
    return a * b


def divide(a: float, b: float) -> float | str:
    """Divide a by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The result of a divided by b, or an error message if b is zero.
    """
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b
