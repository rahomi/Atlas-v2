from atlas.models import Conversation
from atlas.runtime.contracts import ModelClient
from atlas.runtime.model_response import ModelResponse


class AgentRuntime:

    def __init__(
        self,
        model: ModelClient,
    ):
        self._model = model

    async def run(
        self,
        conversation: Conversation,
    ) -> ModelResponse:

        return await self._model.chat(
            conversation
        )