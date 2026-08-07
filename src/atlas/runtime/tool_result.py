from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolResult:
    success: bool
    output: str | None = None
    error: str | None = None

    @classmethod
    def ok(cls, output: str) -> "ToolResult":
        return cls(
            success=True,
            output=output,
        )

    @classmethod
    def fail(cls, error: str) -> "ToolResult":
        return cls(
            success=False,
            error=error,
        )