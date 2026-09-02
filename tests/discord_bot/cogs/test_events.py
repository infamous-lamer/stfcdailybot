import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock

from dailies.collection import EventCollection
from discord_bot.client import Client
from discord_bot.cogs.events import EventsCog

NOW = datetime(2026, 6, 5, 0, 0, tzinfo=UTC)


def test_post_active_events_posts_only_events_active_at_now(event_factory):
    ongoing = event_factory(1, "2026-06-04T16:00:00Z", "2026-06-06T16:00:00Z", title="Ongoing")
    ended = event_factory(2, "2026-06-01T16:00:00Z", "2026-06-02T16:00:00Z", title="Ended")
    upcoming = event_factory(3, "2026-06-06T16:00:00Z", "2026-06-07T16:00:00Z", title="Upcoming")
    events = EventCollection([ongoing, ended, upcoming])
    cog = EventsCog(Client())
    channel = AsyncMock()

    asyncio.run(cog.post_active_events(events, channel, now=NOW))

    channel.send.assert_awaited_once_with("**Ongoing** — active until 2026-06-06T16:00:00+00:00")


def test_post_active_events_returns_next_boundary_time_after_now(event_factory):
    ongoing = event_factory(1, "2026-06-04T16:00:00Z", "2026-06-06T16:00:00Z")
    upcoming = event_factory(3, "2026-06-06T16:00:00Z", "2026-06-07T16:00:00Z")
    events = EventCollection([ongoing, upcoming])
    cog = EventsCog(Client())
    channel = AsyncMock()

    next_post = asyncio.run(cog.post_active_events(events, channel, now=NOW))

    assert next_post == datetime(2026, 6, 6, 16, 0, tzinfo=UTC)


def test_post_active_events_returns_none_when_no_upcoming_boundaries(event_factory):
    ended = event_factory(2, "2026-06-01T16:00:00Z", "2026-06-02T16:00:00Z")
    events = EventCollection([ended])
    cog = EventsCog(Client())
    channel = AsyncMock()

    next_post = asyncio.run(cog.post_active_events(events, channel, now=NOW))

    assert next_post is None
    channel.send.assert_not_awaited()
