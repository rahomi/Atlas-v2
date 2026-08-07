from atlas.runtime.tool_result import ToolResult


def test_success_result():

    result = ToolResult.ok("1200")

    assert result.success is True
    assert result.output == "1200"
    assert result.error is None


def test_failure_result():

    result = ToolResult.fail("Invalid arguments")

    assert result.success is False
    assert result.output is None
    assert result.error == "Invalid arguments"