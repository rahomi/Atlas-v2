from atlas.models import Message, MessageRole


def test_message_creation():

    message = Message(
        role=MessageRole.USER,
        content="Hello Atlas!",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello Atlas!"