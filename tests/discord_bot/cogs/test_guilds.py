import asyncio
import logging
from types import SimpleNamespace

from discord_bot.client import Client
from discord_bot.cogs.guilds import GuildsCog


def test_on_guild_join_logs_the_new_guild(caplog):
    cog = GuildsCog(Client())
    guild = SimpleNamespace(name="Test Guild", id=42, member_count=7)

    with caplog.at_level(logging.INFO, logger="discord_bot.cogs.guilds"):
        asyncio.run(cog.on_guild_join(guild))

    assert "Test Guild" in caplog.text
    assert "42" in caplog.text
    assert "7" in caplog.text
