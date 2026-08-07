import pytest

from atlas.tools import CalculatorTool, ToolRegistry


def test_register_and_get_tool():

    registry = ToolRegistry()

    calculator = CalculatorTool()

    registry.register(calculator)

    result = registry.get("calculator")

    assert result is calculator


def test_list_tools():

    registry = ToolRegistry()

    registry.register(CalculatorTool())

    assert registry.list() == ["calculator"]


def test_duplicate_tool_is_rejected():

    registry = ToolRegistry()

    registry.register(CalculatorTool())

    with pytest.raises(ValueError, match="Tool already registered"):
        registry.register(CalculatorTool())


def test_missing_tool_is_rejected():

    registry = ToolRegistry()

    with pytest.raises(KeyError, match="Tool not found"):
        registry.get("weather")