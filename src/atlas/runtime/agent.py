from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.runtime.contracts import ModelClient, ToolRegistry
from atlas.runtime.model_response import ModelResponse


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
    ) -> ModelResponse:

        while True:

            response = await self._model.chat(
                conversation
            )

            if not response.has_tool_calls:
                return response

            # Only add an assistant message when
            # the model actually produced text.
            if response.content:
                conversation = conversation.append(
                    Message(
                        role=MessageRole.ASSISTANT,
                        content=response.content,
                    )
                )

            for tool_call in response.tool_calls:

                tool = self._tools.get(
                    tool_call.tool_name
                )

                result = await tool.execute(
                    tool_call
                )

                conversation = conversation.append(
                    Message(
                        role=MessageRole.TOOL,
                        content=(
                            result.output
                            if result.success
                            else result.error
                            or "Tool failed"
                        ),
                    )
                )