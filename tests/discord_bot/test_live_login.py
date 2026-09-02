"""Live authentication check against the real Discord API.

Requires DISCORD_BOT_TOKEN in the environment; skipped when it's not set
(e.g. local runs), so this only actually runs where the secret is
available (CI).
"""

import asyncio
import os

import pytest

from discord_bot.client import Client

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")


@pytest.mark.skipif(not DISCORD_BOT_TOKEN, reason="DISCORD_BOT_TOKEN not set")
def test_bot_token_authenticates_with_discord():
    """`login()` only does an HTTP auth check - no gateway connection is opened."""

    async def _login_and_close() -> None:
        client = Client()
        try:
            await client.login(DISCORD_BOT_TOKEN)
        finally:
            await client.close()

    asyncio.run(_login_and_close())
