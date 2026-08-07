import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
    ToolCall,
)
from atlas.runtime.agent import AgentRuntime
from atlas.runtime.contracts import Tool
from atlas.runtime.model_response import ModelResponse
from atlas.runtime.tool_result import ToolResult
from atlas.tools.registry import ToolRegistry


class RecordingModel:

    def __init__(self):
        self.conversations = []
        self.calls = 0
        self.tool_call = ToolCall(
            tool_name="calculator",
            arguments={
                "a": 20,
                "b": 60,
            },
        )

    async def chat(
        self,
        conversation: Conversation,
        tools: tuple[Tool, ...] = (),
    ) -> ModelResponse:

        self.conversations.append(conversation)
        self.calls += 1

        if self.calls == 1:
            return ModelResponse(
                tool_calls=(self.tool_call,)
            )

        return ModelResponse(
            content="The answer is 1200."
        )


class FakeCalculator:

    @property
    def name(self) -> str:
        return "calculator"

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        return ToolResult.ok(
            output="1200",
            tool_call_id=str(tool_call.id),
        )


@pytest.mark.asyncio
async def test_agent_preserves_tool_call_history():

    model = RecordingModel()

    tools = ToolRegistry()
    tools.register(FakeCalculator())

    runtime = AgentRuntime(
        model=model,
        tools=tools,
    )

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Calculate 20 × 60.",
            ),
        )
    )

    response = await runtime.run(
        conversation
    )

    assert response.content == "The answer is 1200."

    # Original conversation is immutable.
    assert len(conversation.messages) == 1

    # Second model call receives the updated history.
    updated = model.conversations[1]

    assert len(updated.messages) == 3

    assistant_message = updated.messages[1]
    tool_message = updated.messages[2]

    assert assistant_message.role == MessageRole.ASSISTANT
    assert assistant_message.content == "Tool call requested."

    assert len(assistant_message.tool_calls) == 1
    assert (
        assistant_message.tool_calls[0].id
        == model.tool_call.id
    )

    assert tool_message.role == MessageRole.TOOL
    assert tool_message.content == "1200"

    assert (
        tool_message.tool_call_id
        == model.tool_call.id
    )