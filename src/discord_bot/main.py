"""Entrypoint for running the STFCDailyBot Discord client.

Usage: poetry run python -m discord_bot.main
"""

from __future__ import annotations

import os

from discord_bot.client import Client


def main() -> None:
    """Read DISCORD_BOT_TOKEN from the environment and run the bot."""
    token = os.environ["DISCORD_BOT_TOKEN"]
    Client().run(token)


if __name__ == "__main__":  # pragma: no cover
    main()
