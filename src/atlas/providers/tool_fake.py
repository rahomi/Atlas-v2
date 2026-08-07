from atlas.models import Conversation, MessageRole
from atlas.runtime.contracts import ModelClient
from atlas.runtime.model_response import ModelResponse
from atlas.models import ToolCall


class FakeToolCallingModel(ModelClient):

    async def chat(
        self,
        conversation: Conversation,
    ) -> ModelResponse:

        if conversation.messages[-1].role == MessageRole.TOOL:

            return ModelResponse(
                content="The answer is 1200."
            )

        return ModelResponse(
            tool_calls=(
                ToolCall(
                    tool_name="calculator",
                    arguments={
                        "a": 25,
                        "b": 48,
                    },
                ),
            )
        )