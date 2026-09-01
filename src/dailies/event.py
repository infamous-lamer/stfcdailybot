"""The Event data model for the STFC.cfd events API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Event(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, frozen=True)

    id: int
    title: str
    description: str | None
    image_url: str | None
    start_time: datetime
    end_time: datetime
    event_type: str
    event_sub_type: str | None
    event_format: str | None
    event_category: str
    priority: str
    min_ops_level: int | None
    max_ops_level: int | None
    repeat_type: str
    repeat_config: dict[str, Any] | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
