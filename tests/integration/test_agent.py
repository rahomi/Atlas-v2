import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.providers.tool_fake import FakeToolCallingModel
from atlas.runtime import AgentRuntime
from atlas.tools import CalculatorTool, ToolRegistry


@pytest.mark.asyncio
async def test_agent_executes_tool_and_returns_final_answer():

    conversation = Conversation()

    conversation = conversation.append(
        Message(
            role=MessageRole.USER,
            content="Calculate 25 times 48.",
        )
    )

    tools = ToolRegistry()

    tools.register(
        CalculatorTool()
    )

    runtime = AgentRuntime(
        model=FakeToolCallingModel(),
        tools=tools,
    )

    response = await runtime.run(
        conversation
    )

    assert response.content == "The answer is 1200."
    assert response.has_tool_calls is False