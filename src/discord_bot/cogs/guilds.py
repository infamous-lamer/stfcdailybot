"""Cog reacting to the bot joining guilds (accepted invitations)."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class GuildsCog(commands.Cog):
    """Handles guild-membership events."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Log when an invitation is accepted and the bot joins a new guild."""
        logger.info("Joined guild %r (id=%s, members=%s)", guild.name, guild.id, guild.member_count)
