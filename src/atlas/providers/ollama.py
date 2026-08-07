from __future__ import annotations

import httpx

from atlas.models import Conversation
from atlas.runtime.model_response import ModelResponse


class OllamaModelClient:

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "qwen3:latest",
    ):
        self._host = host.rstrip("/")
        self._model = model

    async def chat(
        self,
        conversation: Conversation,
    ) -> ModelResponse:

        messages = []

        for message in conversation.messages:

            if message.role.value == "user":
                messages.append(
                    {
                        "role": "user",
                        "content": message.content,
                    }
                )

            elif message.role.value == "assistant":
                messages.append(
                    {
                        "role": "assistant",
                        "content": message.content or "",
                    }
                )

            elif message.role.value == "tool":
                messages.append(
                    {
                        "role": "tool",
                        "content": message.content or "",
                    }
                )

        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{self._host}/api/chat",
                json=payload,
                timeout=300.0,
            )

            response.raise_for_status()

            data = response.json()

        content = data["message"]["content"]

        return ModelResponse(
            content=content,
            tool_calls=(),
        )