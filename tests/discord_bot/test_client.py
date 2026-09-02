import asyncio
import logging
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import discord

from dailies.collection import EventCollection
from dailies.event import Event
from discord_bot.client import Client


def _event(id, start, end, **overrides):
    data = {
        "id": id,
        "title": f"Event {id}",
        "description": None,
        "imageUrl": None,
        "startTime": start,
        "endTime": end,
        "eventType": "hostiles",
        "eventSubType": None,
        "eventFormat": None,
        "eventCategory": "daily",
        "priority": "normal",
        "minOpsLevel": None,
        "maxOpsLevel": None,
        "repeatType": "none",
        "repeatConfig": None,
        "isActive": True,
        "createdAt": start,
        "updatedAt": start,
    }
    data.update(overrides)
    return Event.model_validate(data)


def test_default_command_prefix_is_bang():
    client = Client()

    assert client.command_prefix == "!"


def test_custom_command_prefix():
    client = Client(command_prefix="?")

    assert client.command_prefix == "?"


def test_default_intents_are_discord_default_intents():
    client = Client()

    assert client.intents == discord.Intents.default()


def test_custom_intents_are_used_as_given():
    intents = discord.Intents.none()
    intents.guilds = True

    client = Client(intents=intents)

    assert client.intents == intents


def test_on_guild_join_logs_the_new_guild(caplog):
    client = Client()
    guild = SimpleNamespace(name="Test Guild", id=42, member_count=7)

    with caplog.at_level(logging.INFO, logger="discord_bot.client"):
        asyncio.run(client.on_guild_join(guild))

    assert "Test Guild" in caplog.text
    assert "42" in caplog.text
    assert "7" in caplog.text


def test_invite_url_includes_client_id_and_bot_scopes():
    url = Client.invite_url(123456789)

    assert "client_id=123456789" in url
    assert "scope=bot+applications.commands" in url


def test_invite_url_defaults_to_no_permissions():
    url = Client.invite_url(123456789)

    assert "permissions=0" in url


def test_invite_url_uses_given_permissions():
    permissions = discord.Permissions(send_messages=True)

    url = Client.invite_url(123456789, permissions=permissions)

    assert f"permissions={permissions.value}" in url


ONGOING = _event(1, "2026-06-04T16:00:00Z", "2026-06-06T16:00:00Z", title="Ongoing")
ALREADY_ENDED = _event(2, "2026-06-01T16:00:00Z", "2026-06-02T16:00:00Z", title="Ended")
UPCOMING = _event(3, "2026-06-06T16:00:00Z", "2026-06-07T16:00:00Z", title="Upcoming")
NOW = datetime(2026, 6, 5, 0, 0, tzinfo=UTC)


def test_post_active_events_posts_only_events_active_at_now():
    client = Client()
    events = EventCollection([ONGOING, ALREADY_ENDED, UPCOMING])
    channel = AsyncMock()

    asyncio.run(client.post_active_events(events, channel, now=NOW))

    channel.send.assert_awaited_once_with("**Ongoing** — active until 2026-06-06T16:00:00+00:00")


def test_post_active_events_returns_next_boundary_time_after_now():
    client = Client()
    events = EventCollection([ONGOING, ALREADY_ENDED, UPCOMING])
    channel = AsyncMock()

    next_post = asyncio.run(client.post_active_events(events, channel, now=NOW))

    assert next_post == datetime(2026, 6, 6, 16, 0, tzinfo=UTC)


def test_post_active_events_returns_none_when_no_upcoming_boundaries():
    client = Client()
    events = EventCollection([ALREADY_ENDED])
    channel = AsyncMock()

    next_post = asyncio.run(client.post_active_events(events, channel, now=NOW))

    assert next_post is None
    channel.send.assert_not_awaited()
