import discord
from discord.ext import commands
from pretty_help import Navigation, PrettyHelp, __version__

def test_version():
    assert __version__ == "1.1.0"


# replace with your token
TOKEN = "TOKEN"

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
nav = Navigation(":discord:743511195197374563", "👎", "\U0001F44D")


bot = commands.Bot(command_prefix="!", description="this is the bots descripton")
bot.help_command = PrettyHelp(navigation=nav)


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    print(f"With ID: {bot.user.id}")


class TestCog(commands.Cog):
    """This is a cog for testing purposes"""

    @commands.command()
    async def testcommand(self, ctx: commands.Context):
        await ctx.send("This is a test command")


class ACog(commands.Cog, name="Z Cog"):
    """This is a cog for testing purposes"""

    @commands.group()
    async def atestcommand(self, ctx: commands.Context):
        await ctx.send("This is a test command")

    @atestcommand.command()
    async def atestgroupcommand(self, ctx):
        await ctx.send("this is a subcommand")


@bot.command()
async def test(ctx: commands.Context):
    await ctx.send("this is the test command")


bot.add_cog(TestCog(bot))
bot.add_cog(ACog(bot))
bot.run(TOKEN)

# run !help in discord after starting the script
