from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class ToolCall(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4
    )

    tool_name: str = Field(
        min_length=1
    )

    arguments: dict[str, Any] = {}