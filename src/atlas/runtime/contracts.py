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
        tools: tuple[Tool, ...] = (),
    ) -> ModelResponse:
        ...


class Tool(Protocol):

    @property
    def name(self) -> str:
        ...

    @property
    def definition(self) -> dict[str, Any]:
        ...

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        ...