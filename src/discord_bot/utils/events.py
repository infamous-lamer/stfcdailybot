"""Pure event-scheduling/formatting helpers.

No discord.py dependency, so these are testable without mocking any
Discord objects - the cogs that use them own the actual I/O.
"""

from __future__ import annotations

from datetime import datetime

from dailies.collection import EventCollection
from dailies.event import Event


def next_post_time(events: EventCollection, now: datetime) -> datetime | None:
    """The earliest of `events`' start/end boundaries after `now`, or `None`."""
    upcoming = [t for t in (*events.start_times, *events.end_times) if t > now]
    return min(upcoming) if upcoming else None


def format_event(event: Event) -> str:
    """Render `event` as the message text used to announce it."""
    return f"**{event.title}** — active until {event.end_time.isoformat()}"
