from pydantic import BaseModel, Field


class CalculatorArguments(BaseModel):
    a: float = Field(
        description="First number"
    )

    b: float = Field(
        description="Second number"
    )