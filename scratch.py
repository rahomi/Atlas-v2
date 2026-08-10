import asyncio

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
)
from atlas.providers.ollama import OllamaModelClient
from atlas.runtime.agent import AgentRuntime
from atlas.tools import CalculatorTool, ToolRegistry


async def main():

    conversation = Conversation()

    conversation = conversation.append(
        Message(
            role=MessageRole.USER,
            content=(
                "Use the calculator tool to calculate "
                "1234567 × 89123. Do not calculate it yourself."
            ),
        )
    )

    model = OllamaModelClient(
        model="qwen3:latest"
    )

    tools = ToolRegistry()
    tools.register(CalculatorTool())

    runtime = AgentRuntime(
        model=model,
        tools=tools,
    )

    response = await runtime.run(
        conversation
    )

    print()
    print("MODEL RESPONSE:")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())