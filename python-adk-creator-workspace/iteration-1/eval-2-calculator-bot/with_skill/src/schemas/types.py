"""Type definitions and Pydantic models for the Calculator Bot.

This module defines structured data types used throughout the application.
Can be extended with Pydantic models for validation and serialization.
"""

from typing import Union, List, Optional
from dataclasses import dataclass


@dataclass
class CalculationResult:
    """Represents the result of a calculation operation."""

    operation: str
    operands: List[Union[int, float]]
    result: Union[int, float]
    error: Optional[str] = None

    def __str__(self) -> str:
        """String representation of the calculation result."""
        if self.error:
            return f"Error in {self.operation}: {self.error}"
        return f"{self.operation}({', '.join(map(str, self.operands))}) = {self.result}"
