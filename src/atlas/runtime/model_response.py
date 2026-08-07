from __future__ import annotations

from dataclasses import dataclass

from atlas.models import ToolCall


@dataclass(frozen=True)
class ModelResponse:
    content: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)