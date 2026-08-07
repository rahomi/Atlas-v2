from __future__ import annotations

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.runtime.contracts import ModelClient
from atlas.runtime.tool_result import ToolResult
from atlas.tools.registry import ToolRegistry


class AgentRuntime:

    def __init__(
        self,
        model: ModelClient,
        tools: ToolRegistry,
        max_iterations: int = 10,
    ):
        if max_iterations < 1:
            raise ValueError(
                "max_iterations must be at least 1"
            )

        self._model = model
        self._tools = tools
        self._max_iterations = max_iterations

    async def run(
        self,
        conversation: Conversation,
    ):
        current = conversation

        for _ in range(self._max_iterations):

            response = await self._model.chat(
                current
            )

            if not response.tool_calls:
                return response

            current = await self._execute_tool_calls(
                current,
                response,
            )

        raise RuntimeError(
            "Agent exceeded maximum iterations"
        )

    async def _execute_tool_calls(
        self,
        conversation: Conversation,
        response,
    ) -> Conversation:

        current = conversation

        current = current.append(
            Message(
                role=MessageRole.ASSISTANT,
                content=(
                    response.content
                    or "Tool call requested."
                ),
                tool_calls=response.tool_calls,
            )
        )

        for tool_call in response.tool_calls:

            try:
                tool = self._tools.get(
                    tool_call.tool_name
                )

                result = await tool.execute(
                    tool_call
                )

            except KeyError as exc:
                result = ToolResult.fail(
                    error=str(exc),
                    tool_call_id=tool_call.id,
                )

            except Exception as exc:
                result = ToolResult.fail(
                    error=f"Tool error: {exc}",
                    tool_call_id=tool_call.id,
                )

            current = current.append(
                Message(
                    role=MessageRole.TOOL,
                    content=(
                        result.output
                        if result.success
                        else result.error
                        or "Tool execution failed."
                    ),
                    tool_call_id=tool_call.id,
                )
            )

        return current