"""Discord client for STFCDailyBot.

Wraps `discord.ext.commands.Bot` (discord.py's command-capable client)
rather than the lower-level `discord.Client`, so future prefix/slash
commands can register directly on this class via cogs.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import ClassVar

import discord
from discord.ext import commands

from dailies.collection import EventCollection
from dailies.event import Event

logger = logging.getLogger(__name__)


class Client(commands.Bot):
    """The STFCDailyBot Discord client."""

    DEFAULT_COMMAND_PREFIX: ClassVar[str] = "!"

    def __init__(
        self,
        *,
        command_prefix: str = DEFAULT_COMMAND_PREFIX,
        intents: discord.Intents | None = None,
    ) -> None:
        super().__init__(command_prefix=command_prefix, intents=intents or discord.Intents.default())

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Log when an invitation is accepted and the bot joins a new guild."""
        logger.info("Joined guild %r (id=%s, members=%s)", guild.name, guild.id, guild.member_count)

    @staticmethod
    def invite_url(client_id: int, *, permissions: discord.Permissions | None = None) -> str:
        """Build an OAuth2 URL for inviting this bot (by application client ID) to a guild."""
        return discord.utils.oauth_url(
            client_id,
            permissions=permissions or discord.Permissions.none(),
            scopes=("bot", "applications.commands"),
        )

    async def post_active_events(
        self,
        events: EventCollection,
        channel: discord.abc.Messageable,
        *,
        now: datetime | None = None,
    ) -> datetime | None:
        """Post events active at `now` to `channel`.

        Returns the next timestamp at which the active set changes (the
        next event start or end after `now`), or `None` if there isn't
        one — i.e. when to call this again to keep the channel current.
        """
        now = now or datetime.now(UTC)
        for event in events.at(now):
            await channel.send(self._format_event(event))
        return self._next_post_time(events, now)

    @staticmethod
    def _next_post_time(events: EventCollection, now: datetime) -> datetime | None:
        upcoming = [t for t in (*events.start_times, *events.end_times) if t > now]
        return min(upcoming) if upcoming else None

    @staticmethod
    def _format_event(event: Event) -> str:
        return f"**{event.title}** — active until {event.end_time.isoformat()}"
