"""Discord client for STFCDailyBot.

Wraps `discord.ext.commands.Bot` (discord.py's command-capable client)
rather than the lower-level `discord.Client`, so future prefix/slash
commands can register directly on this class via cogs.
"""

from __future__ import annotations

from typing import ClassVar

import discord
from discord.ext import commands

from discord_bot.cogs.events import EventsCog
from discord_bot.cogs.guilds import GuildsCog


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

    async def setup_hook(self) -> None:
        """Load cogs before the bot connects to the gateway."""
        await self.add_cog(GuildsCog(self))
        await self.add_cog(EventsCog(self))

    @staticmethod
    def invite_url(client_id: int, *, permissions: discord.Permissions | None = None) -> str:
        """Build an OAuth2 URL for inviting this bot (by application client ID) to a guild."""
        return discord.utils.oauth_url(
            client_id,
            permissions=permissions or discord.Permissions.none(),
            scopes=("bot", "applications.commands"),
        )
