from atlas.models import Conversation
from atlas.runtime.contracts import ModelClient


class AgentRuntime:

    def __init__(
        self,
        model: ModelClient,
    ):
        self._model = model

    async def run(
        self,
        conversation: Conversation,
    ) -> str:

        return await self._model.chat(conversation)