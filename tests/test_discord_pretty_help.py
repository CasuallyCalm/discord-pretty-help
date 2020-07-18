from pretty_help import __version__, PrettyHelp


def test_version():
    assert __version__ == "0.1.0"


import discord
from discord.ext import commands

# replace with your token
TOKEN = "TOKEN"
bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    print(f"With ID: {bot.user.id}")


bot.run(TOKEN)

# run !help in discord after starting the script

