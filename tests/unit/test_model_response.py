from atlas.runtime.model_response import ModelResponse
from atlas.models import ToolCall


def test_model_response_without_tools():

    response = ModelResponse(
        content="Hello"
    )

    assert response.content == "Hello"
    assert response.has_tool_calls is False


def test_model_response_with_tool_call():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": 25,
            "b": 48,
        },
    )

    response = ModelResponse(
        tool_calls=(tool_call,)
    )

    assert response.has_tool_calls is True
    assert response.tool_calls[0].tool_name == "calculator"