from __future__ import annotations

from typing import Any, Protocol

from atlas.models import Conversation
from atlas.runtime.model_response import ModelResponse
from atlas.models import ToolCall

from .tool_result import ToolResult


class ModelClient(Protocol):
    """
    Every AI model provider must implement this contract.
    """

    async def chat(
        self,
        conversation: Conversation,
    ) -> ModelResponse:
        ...


class Tool(Protocol):
    """
    Contract for every executable tool.
    """

    @property
    def name(self) -> str:
        ...

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        ...

class ToolRegistry(Protocol):
    """
    Registry responsible for managing tools.
    """

    def register(
        self,
        tool: Tool,
    ) -> None:
        ...

    def get(
        self,
        name: str,
    ) -> Tool:
        ...

    def list(self) -> list[str]:
        ...


class Memory(Protocol):
    """
    Contract for conversation persistence.
    """

    async def load(
        self,
        conversation_id: str,
    ) -> Conversation:
        ...

    async def save(
        self,
        conversation: Conversation,
    ) -> None:
        ...