from pydantic import BaseModel


class CalculationResult(BaseModel):
    """Schema for a calculation result."""

    operation: str
    operand_a: float
    operand_b: float
    result: float
