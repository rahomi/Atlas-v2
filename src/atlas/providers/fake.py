from atlas.models import Conversation
from atlas.runtime.contracts import ModelClient


class FakeModelClient(ModelClient):

    async def chat(
        self,
        conversation: Conversation,
    ) -> str:

        last = conversation.messages[-1]

        return f"Echo: {last.content}"