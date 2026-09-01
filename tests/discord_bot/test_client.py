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
