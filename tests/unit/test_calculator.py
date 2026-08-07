import pytest
from atlas.models import ToolCall
from atlas.tools import CalculatorTool


@pytest.mark.asyncio
async def test_calculator_multiplies():

    calculator = CalculatorTool()

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": 25,
            "b": 48,
        },
    )

    result = await calculator.execute(
        tool_call
    )

    assert result.success is True
    assert result.output == "1200.0"
    assert result.error is None
    assert result.tool_call_id == tool_call.id


@pytest.mark.asyncio
async def test_calculator_rejects_invalid_arguments():

    calculator = CalculatorTool()

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": "hello",
            "b": 48,
        },
    )

    result = await calculator.execute(
        tool_call
    )

    assert result.success is False
    assert result.output is None
    assert result.error is not None
    assert result.tool_call_id == tool_call.id