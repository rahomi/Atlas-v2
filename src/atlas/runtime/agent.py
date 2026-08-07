from __future__ import annotations

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.runtime.contracts import ModelClient
from atlas.tools.registry import ToolRegistry


class AgentRuntime:

    def __init__(
        self,
        model: ModelClient,
        tools: ToolRegistry,
    ):
        self._model = model
        self._tools = tools

    async def run(
        self,
        conversation: Conversation,
    ):
        current = conversation

        while True:

            response = await self._model.chat(
                current
            )

            if not response.tool_calls:
                return response

            for tool_call in response.tool_calls:

                tool = self._tools.get(
                    tool_call.tool_name
                )

                result = await tool.execute(
                    tool_call
                )

                current = current.append(
                    Message(
                        role=MessageRole.ASSISTANT,
                        content=(
                            response.content
                            or "Tool call requested."
                        ),
                        tool_calls=(tool_call,),
                    )
                )

                current = current.append(
                    Message(
                        role=MessageRole.TOOL,
                        content=result.output,
                        tool_call_id=tool_call.id,
                    )
                )