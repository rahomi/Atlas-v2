from atlas.models import Conversation, Message, MessageRole
from atlas.runtime.agent import AgentRuntime
from atlas.runtime.contracts import Tool
from atlas.runtime.model_response import ModelResponse
from atlas.tools import CalculatorTool, ToolRegistry
from atlas.models import ToolCall


class LoopingModelClient:

    async def chat(
        self,
        conversation: Conversation,
        tools: tuple[Tool, ...] = (),
    ) -> ModelResponse:

        return ModelResponse(
            content="",
            tool_calls=(
                ToolCall(
                    tool_name="calculator",
                    arguments={
                        "a": 10,
                        "b": 20,
                        "operation": "multiply",
                    },
                ),
            ),
        )


async def test_agent_stops_after_max_iterations():

    model = LoopingModelClient()

    tools = ToolRegistry()
    tools.register(
        CalculatorTool()
    )

    runtime = AgentRuntime(
        model=model,
        tools=tools,
        max_iterations=3,
    )

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Calculate 10 * 20",
            ),
        )
    )

    try:
        await runtime.run(conversation)
    except RuntimeError as exc:
        assert str(exc) == (
            "Agent exceeded maximum iterations"
        )
    else:
        raise AssertionError(
            "Agent should have stopped after "
            "maximum iterations"
        )