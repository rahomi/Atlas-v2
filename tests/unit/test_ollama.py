import httpx
import pytest

from atlas.models import (
    Conversation,
    Message,
    MessageRole,
    ToolCall,
)
from atlas.providers.ollama import OllamaModelClient
from atlas.tools.calculator import CalculatorTool


@pytest.mark.asyncio
async def test_ollama_returns_text_response(monkeypatch):

    class FakeResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {
                    "role": "assistant",
                    "content": "Hello!",
                }
            }

    async def fake_post(
        self,
        url,
        **kwargs,
    ):
        assert url == "http://localhost:11434/api/chat"

        assert kwargs["json"]["model"] == "qwen3:latest"
        assert kwargs["json"]["stream"] is False

        return FakeResponse()

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        fake_post,
    )

    client = OllamaModelClient()

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Hello",
            ),
        )
    )

    response = await client.chat(
        conversation
    )

    assert response.content == "Hello!"
    assert response.tool_calls == ()

@pytest.mark.asyncio
async def test_ollama_parses_tool_call(monkeypatch):

    class FakeResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "function": {
                                "name": "calculator",
                                "arguments": {
                                    "a": 20,
                                    "b": 60,
                                },
                            }
                        }
                    ],
                }
            }

    async def fake_post(
        self,
        url,
        **kwargs,
    ):
        return FakeResponse()

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        fake_post,
    )

    client = OllamaModelClient()

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Calculate 20 times 60.",
            ),
        )
    )

    response = await client.chat(
        conversation
    )

    assert response.content == ""

    assert len(response.tool_calls) == 1

    tool_call = response.tool_calls[0]

    assert tool_call.tool_name == "calculator"
    assert tool_call.arguments == {
        "a": 20,
        "b": 60,
    }

@pytest.mark.asyncio
async def test_ollama_sends_tools(monkeypatch):

    captured = {}

    class FakeResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {
                    "role": "assistant",
                    "content": "Hello!",
                }
            }

    async def fake_post(
        self,
        url,
        **kwargs,
    ):
        captured["payload"] = kwargs["json"]
        return FakeResponse()

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        fake_post,
    )

    client = OllamaModelClient()

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.USER,
                content="Calculate something.",
            ),
        )
    )

    calculator = CalculatorTool()

    response = await client.chat(
        conversation,
        tools=(calculator,),
    )

    assert response.content == "Hello!"

    payload = captured["payload"]

    assert "tools" in payload
    assert len(payload["tools"]) == 1

    tool = payload["tools"][0]

    assert tool["type"] == "function"
    assert tool["function"]["name"] == "calculator"