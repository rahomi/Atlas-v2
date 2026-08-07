import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
    ToolCall,
)
from atlas.runtime.agent import AgentRuntime
from atlas.runtime.model_response import ModelResponse
from atlas.runtime.tool_result import ToolResult
from atlas.tools.registry import ToolRegistry


class RecordingTool:

    def __init__(self, name: str, output: str):
        self._name = name
        self._output = output
        self.calls = []

    @property
    def name(self) -> str:
        return self._name

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        self.calls.append(tool_call)

        return ToolResult.ok(
            output=self._output,
            tool_call_id=str(tool_call.id),
        )


class MultipleToolModel:

    def __init__(self):
        self.calls = 0
        self.conversations = []

        self.first_call = ToolCall(
            tool_name="calculator_a",
            arguments={"value": 100},
        )

        self.second_call = ToolCall(
            tool_name="calculator_b",
            arguments={"value": 200},
        )

    async def chat(
        self,
        conversation: Conversation,
    ) -> ModelResponse:

        self.conversations.append(conversation)
        self.calls += 1

        if self.calls == 1:
            return ModelResponse(
                tool_calls=(
                    self.first_call,
                    self.second_call,
                )
            )

        return ModelResponse(
            content="Both tools completed."
        )


@pytest.mark.asyncio
async def test_agent_executes_multiple_tools_in_order():

    model = MultipleToolModel()

    tool_a = RecordingTool(
        "calculator_a",
        "100",
    )

    tool_b = RecordingTool(
        "calculator_b",
        "200",
    )

    tools = ToolRegistry()
    tools.register(tool_a)
    tools.register(tool_b)

    runtime = AgentRuntime(
        model=model,
        tools=tools,
    )

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Run both calculations.",
            ),
        )
    )

    response = await runtime.run(
        conversation
    )

    assert response.content == (
        "Both tools completed."
    )

    # Both tools were executed exactly once.
    assert len(tool_a.calls) == 1
    assert len(tool_b.calls) == 1

    # Correct ToolCalls reached the correct tools.
    assert tool_a.calls[0].id == model.first_call.id
    assert tool_b.calls[0].id == model.second_call.id

    # The second model call receives the complete history.
    updated = model.conversations[1]

    assert len(updated.messages) == 4

    assistant_message = updated.messages[1]
    first_tool_message = updated.messages[2]
    second_tool_message = updated.messages[3]

    # Assistant preserved both calls.
    assert assistant_message.role == MessageRole.ASSISTANT
    assert len(assistant_message.tool_calls) == 2

    assert (
        assistant_message.tool_calls[0].id
        == model.first_call.id
    )

    assert (
        assistant_message.tool_calls[1].id
        == model.second_call.id
    )

    # Tool results preserve order.
    assert first_tool_message.role == MessageRole.TOOL
    assert first_tool_message.content == "100"
    assert (
        first_tool_message.tool_call_id
        == model.first_call.id
    )

    assert second_tool_message.role == MessageRole.TOOL
    assert second_tool_message.content == "200"
    assert (
        second_tool_message.tool_call_id
        == model.second_call.id
    )