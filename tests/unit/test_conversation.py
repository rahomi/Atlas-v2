from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)


def test_append_message():

    conversation = Conversation()

    updated = conversation.append(
        Message(
            role=MessageRole.USER,
            content="Hello"
        )
    )

    assert len(conversation.messages) == 0

    assert len(updated.messages) == 1