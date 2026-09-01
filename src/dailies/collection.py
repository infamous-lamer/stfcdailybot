"""An ordered collection of Event records with time/category/activity lookups."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import datetime
from functools import cached_property

from pydantic import TypeAdapter

from dailies.client import Client
from dailies.event import Event

_EventList = TypeAdapter(list[Event])


class EventCollection:
    """Events kept sorted by start_time, with chainable filters."""

    def __init__(self, events: Iterable[Event] = ()) -> None:
        self._events: tuple[Event, ...] = tuple(sorted(events, key=lambda e: e.start_time))

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self) -> Iterator[Event]:
        return iter(self._events)

    def __getitem__(self, index: int) -> Event:
        return self._events[index]

    @classmethod
    def fetch(cls, client: Client | None = None) -> EventCollection:
        """Fetch and parse all events from the API into a collection."""
        client = client or Client()
        return cls(_EventList.validate_python(client.fetch_events()))

    def at(self, event_time: datetime) -> EventCollection:
        """Events active at the given point in time (start_time <= event_time < end_time)."""
        return EventCollection(e for e in self._events if e.start_time <= event_time < e.end_time)

    def _where(self, attr: str, value: object) -> EventCollection:
        return EventCollection(e for e in self._events if getattr(e, attr) == value)

    def by_category(self, event_category: str) -> EventCollection:
        """Events whose event_category matches exactly."""
        return self._where("event_category", event_category)

    def by_active(self, is_active: bool = True) -> EventCollection:
        """Events whose is_active flag matches."""
        return self._where("is_active", is_active)

    def by_priority(self, priority: str) -> EventCollection:
        """Events whose priority matches exactly."""
        return self._where("priority", priority)

    def _unique_sorted(self, attr: str) -> list[datetime]:
        return sorted({getattr(e, attr) for e in self._events})

    @cached_property
    def start_times(self) -> list[datetime]:
        """All unique start_time values across the collection, sorted ascending."""
        return self._unique_sorted("start_time")

    @cached_property
    def end_times(self) -> list[datetime]:
        """All unique end_time values across the collection, sorted ascending."""
        return self._unique_sorted("end_time")
