import asyncio

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.providers.ollama import OllamaModelClient


async def main():

    conversation = Conversation()

    conversation = conversation.append(
        Message(
            role=MessageRole.USER,
            content="What is 25 multiplied by 48?",
        )
    )

    client = OllamaModelClient(
        model="qwen3:latest"
    )

    response = await client.chat(
        conversation
    )

    print()
    print("MODEL RESPONSE:")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())