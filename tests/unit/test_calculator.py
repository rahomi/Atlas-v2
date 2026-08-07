import pytest

from atlas.tools import CalculatorTool


@pytest.mark.asyncio
async def test_calculator_multiplies():

    calculator = CalculatorTool()

    result = await calculator.execute(
        {
            "a": 25,
            "b": 48,
        }
    )

    assert result.success is True
    assert result.output == "1200.0"

@pytest.mark.asyncio
async def test_calculator_rejects_invalid_arguments():

    calculator = CalculatorTool()

    result = await calculator.execute(
        {
            "a": "hello",
            "b": 48,
        }
    )

    assert result.success is False
    assert result.output is None
    assert result.error is not None@pytest.mark.asyncio
    
async def test_calculator_rejects_invalid_arguments():

    calculator = CalculatorTool()

    result = await calculator.execute(
        {
            "a": "hello",
            "b": 48,
        }
    )

    assert result.success is False
    assert result.output is None
    assert result.error is not None