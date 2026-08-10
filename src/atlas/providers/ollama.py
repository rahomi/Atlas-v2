from __future__ import annotations

import httpx

from atlas.models import Conversation, ToolCall
from atlas.runtime.contracts import Tool
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
        tools=(),
    ) -> ModelResponse:

        messages = []

        for message in conversation.messages:
            if message.role.value == "system":
                messages.append({
                    "role": "system",
                    "content": message.content,
                })
            elif message.role.value == "user":
                messages.append({
                    "role": "user",
                    "content": message.content,
                })
            elif message.role.value == "assistant":
                msg = {
                    "role": "assistant",
                    "content": message.content or "",
                }
                # IMPORTANT: Send back the tool_calls the assistant made!
                if message.tool_calls:
                    msg["tool_calls"] = [
                        {
                            "type": "function",
                            "function": {
                                "name": call.tool_name,
                                "arguments": call.arguments,
                            }
                        }
                        for call in message.tool_calls
                    ]
                messages.append(msg)
            elif message.role.value == "tool":
                messages.append({
                    "role": "tool",
                    "content": message.content or "",
                })

        ollama_tools = [
            {
                "type": "function",
                "function": tool.definition,
            }
            for tool in tools
        ]

        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "think": False,
            "tools": ollama_tools,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._host}/api/chat",
                json=payload,
                timeout=300.0,
            )

            response.raise_for_status()

            data = response.json()
        
        print(f"\n[RAW OLLAMA RESPONSE]: {data}\n")
        
        message = data["message"]

        content = message.get("content") or ""

        tool_calls = tuple(
            ToolCall(
                tool_name=call["function"]["name"],
                arguments=call["function"].get("arguments", {}),
            )
            for call in message.get("tool_calls", [])
        )

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
        )