import asyncio
import logging
from types import SimpleNamespace

import discord

from discord_bot.client import Client


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
