"""Cog posting an EventCollection's currently-active events to a channel."""

from __future__ import annotations

from datetime import UTC, datetime

import discord
from discord.ext import commands

from dailies.collection import EventCollection
from discord_bot.utils.events import format_event, next_post_time


class EventsCog(commands.Cog):
    """Posts active STFC events to a Discord channel."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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
            await channel.send(format_event(event))
        return next_post_time(events, now)
