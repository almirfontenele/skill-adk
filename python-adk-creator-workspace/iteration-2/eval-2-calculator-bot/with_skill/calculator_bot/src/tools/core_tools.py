def add(a: float, b: float) -> float:
    """Adds two numbers and returns the result.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first and returns the result.

    Args:
        a: The number to subtract from.
        b: The number to subtract.

    Returns:
        The result of a minus b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiplies two numbers and returns the result.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product of a and b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Divides the first number by the second and returns the result.

    Args:
        a: The dividend.
        b: The divisor (must not be zero).

    Returns:
        The result of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
