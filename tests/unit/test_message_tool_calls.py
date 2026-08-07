from atlas.models import Message, MessageRole
from atlas.models import ToolCall


def test_assistant_message_can_contain_tool_call():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": 25,
            "b": 48,
        },
    )

    message = Message(
        role=MessageRole.ASSISTANT,
        tool_calls=(tool_call,),
    )

    assert message.content is None
    assert len(message.tool_calls) == 1
    assert message.tool_calls[0].tool_name == "calculator"


def test_tool_message_references_tool_call():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": 25,
            "b": 48,
        },
    )

    message = Message(
        role=MessageRole.TOOL,
        content="1200.0",
        tool_call_id=tool_call.id,
    )

    assert message.content == "1200.0"
    assert message.tool_call_id == tool_call.id