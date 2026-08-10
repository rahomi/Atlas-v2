from pydantic import BaseModel, Field


class CalculatorArguments(BaseModel):
    a: int = Field(
        description="First number"
    )

    b: int = Field(
        description="Second number"
    )