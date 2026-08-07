from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    success: bool
    output: str | None = None
    error: str | None = None
    tool_call_id: str | None = None

    @classmethod
    def ok(
        cls,
        output: str,
        tool_call_id: str | None = None,
    ) -> "ToolResult":
        return cls(
            success=True,
            output=output,
            tool_call_id=tool_call_id,
        )

    @classmethod
    def fail(
        cls,
        error: str,
        tool_call_id: str | None = None,
    ) -> "ToolResult":
        return cls(
            success=False,
            error=error,
            tool_call_id=tool_call_id,
        )