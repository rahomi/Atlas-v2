from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @property
    def is_failure(self) -> bool:
        return self.error is not None

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def fail(cls, error: str) -> "Result[T]":
        return cls(error=error)