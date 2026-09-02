from datetime import UTC, datetime

from dailies.collection import EventCollection
from discord_bot.utils.events import format_event, next_post_time

NOW = datetime(2026, 6, 5, 0, 0, tzinfo=UTC)


def test_format_event_includes_title_and_end_time(event_factory):
    event = event_factory(1, "2026-06-04T16:00:00Z", "2026-06-06T16:00:00Z", title="Ongoing")

    assert format_event(event) == "**Ongoing** — active until 2026-06-06T16:00:00+00:00"


def test_next_post_time_returns_earliest_boundary_after_now(event_factory):
    ongoing = event_factory(1, "2026-06-04T16:00:00Z", "2026-06-06T16:00:00Z")
    upcoming = event_factory(3, "2026-06-06T16:00:00Z", "2026-06-07T16:00:00Z")
    events = EventCollection([ongoing, upcoming])

    assert next_post_time(events, NOW) == datetime(2026, 6, 6, 16, 0, tzinfo=UTC)


def test_next_post_time_returns_none_when_no_upcoming_boundaries(event_factory):
    ended = event_factory(2, "2026-06-01T16:00:00Z", "2026-06-02T16:00:00Z")
    events = EventCollection([ended])

    assert next_post_time(events, NOW) is None
