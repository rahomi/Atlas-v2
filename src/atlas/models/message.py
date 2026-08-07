from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from .roles import MessageRole
from .tool_call import ToolCall


class Message(BaseModel):
    """
    A single message in a conversation.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4
    )

    role: MessageRole

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    tool_calls: tuple[ToolCall, ...] = ()

    tool_call_id: UUID | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )