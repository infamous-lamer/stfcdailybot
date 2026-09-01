"""Discord client for STFCDailyBot.

Wraps `discord.ext.commands.Bot` (discord.py's command-capable client)
rather than the lower-level `discord.Client`, so future prefix/slash
commands can register directly on this class via cogs.
"""

from __future__ import annotations

from typing import ClassVar

import discord
from discord.ext import commands


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
