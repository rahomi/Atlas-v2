from atlas.models import Conversation
from atlas.runtime.contracts import ModelClient, Tool
from atlas.runtime.model_response import ModelResponse


class FakeModelClient(ModelClient):

    async def chat(
        self,
        conversation: Conversation,
        tools: tuple[Tool, ...] = (),
    ) -> ModelResponse:

        last = conversation.messages[-1]

        return ModelResponse(
            content=f"Echo: {last.content}"
        )