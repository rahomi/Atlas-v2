import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
    ToolCall,
)
from atlas.runtime.agent import AgentRuntime
from atlas.runtime.model_response import ModelResponse
from atlas.tools.registry import ToolRegistry


class UnknownToolModel:

    def __init__(self):
        self.calls = 0

    async def chat(
        self,
        conversation: Conversation,
    ) -> ModelResponse:

        self.calls += 1

        if self.calls == 1:
            return ModelResponse(
                content="",
                tool_calls=(
                    ToolCall(
                        tool_name="weather",
                        arguments={
                            "city": "Dhaka",
                        },
                    ),
                ),
            )

        return ModelResponse(
            content="I cannot access the weather tool."
        )


@pytest.mark.asyncio
async def test_agent_handles_unknown_tool():

    model = UnknownToolModel()

    tools = ToolRegistry()

    runtime = AgentRuntime(
        model=model,
        tools=tools,
    )

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="What is the weather in Dhaka?",
            ),
        )
    )

    response = await runtime.run(
        conversation
    )

    assert response.content == (
        "I cannot access the weather tool."
    )