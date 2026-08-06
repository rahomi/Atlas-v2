from __future__ import annotations

from typing import Any, Protocol

from atlas.models import Conversation


class ModelClient(Protocol):
    """
    Every AI model provider must implement this contract.
    """

    async def chat(
        self,
        conversation: Conversation,
    ) -> str:
        ...

class ToolRegistry(Protocol):

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


class Tool(Protocol):

    @property
    def name(self) -> str:
        ...

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> Any:
        ...

    from atlas.models import Conversation


class Memory(Protocol):

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