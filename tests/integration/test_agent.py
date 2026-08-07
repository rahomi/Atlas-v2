import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.providers.fake import FakeModelClient
from atlas.runtime import AgentRuntime


@pytest.mark.asyncio
async def test_agent_returns_response():

    conversation = Conversation()

    conversation = conversation.append(
        Message(
            role=MessageRole.USER,
            content="Hello!"
        )
    )

    runtime = AgentRuntime(
        FakeModelClient()
    )

    response = await runtime.run(
        conversation
    )

    assert response == "Echo: Hello!"