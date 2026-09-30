from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Lane(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class CamelModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        ser_json_timedelta="iso8601",
    )


class HealthResponse(CamelModel):
    status: str


class Card(CamelModel):
    id: str
    title: str
    lane: Lane
    position: int
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt", serialization_alias="updatedAt")


class CreateCardRequest(CamelModel):
    title: str
    lane: Optional[Lane] = Lane.todo

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed or len(trimmed) > 200:
            raise ValueError("Title must be 1–200 characters")
        return trimmed


class UpdateCardRequest(CamelModel):
    title: Optional[str] = None
    lane: Optional[Lane] = None
    position: Optional[int] = Field(default=None, ge=0)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        trimmed = value.strip()
        if not trimmed or len(trimmed) > 200:
            raise ValueError("Title must be 1–200 characters")
        return trimmed
