from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from .message import Message


class Conversation(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(default_factory=uuid4)

    messages: tuple[Message, ...] = ()

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def append(
        self,
        message: Message,
    ) -> "Conversation":

        return self.model_copy(
            update={
                "messages": (
                    *self.messages,
                    message,
                )
            }
        )