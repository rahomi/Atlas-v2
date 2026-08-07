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


class FailingTool:

    @property
    def name(self) -> str:
        return "failing"

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        raise RuntimeError(
            "Something went wrong"
        )


class RecoveryModel:

    def __init__(self):
        self.calls = 0

    async def chat(
            self,
            conversation: Conversation,
            tools: tuple[Tool, ...] = (),
        ) -> ModelResponse:

        self.calls += 1

        if self.calls == 1:
            return ModelResponse(
                content="",
                tool_calls=(
                    ToolCall(
                        tool_name="failing",
                        arguments={},
                    ),
                ),
            )

        return ModelResponse(
            content="Recovered successfully."
        )


class SimpleToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name):
        return self._tools[name]

    def list(self):
        return list(self._tools.keys())


@pytest.mark.asyncio
async def test_agent_handles_tool_exception():

    model = RecoveryModel()

    tools = SimpleToolRegistry()
    tools.register(FailingTool())

    runtime = AgentRuntime(
        model=model,
        tools=tools,
    )

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Use the failing tool.",
            ),
        )
    )

    response = await runtime.run(
        conversation
    )

    assert response.content == (
        "Recovered successfully."
    )