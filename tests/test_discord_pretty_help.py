"""
Note: Rename `env.example` to `.env` and enter your token then run `poetry run test` in your terminal
"""
import os

from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
import dotenv

dotenv.load_dotenv("./tests/.env")

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
menu = DefaultMenu(
    "\U0001F44D",
    "👎",
    ":discord:743511195197374563",
    active_time=5,
    delete_after_timeout=True,
)

# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

bot = commands.Bot(
    command_prefix="!",
    description="this is the bots descripton",
)
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)
# bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note, show_index=False)


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    print(f"With ID: {bot.user.id}")


class TestCog(commands.Cog):
    """This is a cog for testing purposes"""

    @commands.command(description="This is a command description")
    async def testcommand(self, ctx: commands.Context):
        """This is command help"""
        await ctx.send("This is a test command")

    @commands.command(description="This is a command description")
    async def testcommand2(self, ctx: commands.Context):
        await ctx.send("This is a test command")

    @commands.command()
    async def testcommand3(self, ctx: commands.Context):
        """This is command help"""
        await ctx.send("This is a test command")


class ACog(commands.Cog, name="Z Cog"):
    """This is a cog for testing purposes"""

    @commands.group(description="This is a group description")
    async def atestcommand(self, ctx: commands.Context):
        """This is group help"""
        await ctx.send("This is a test command")

    @atestcommand.command()
    async def atestgroupcommand(self, ctx):
        await ctx.send("this is a subcommand")


class LargeCog(commands.Cog):
    @commands.command()
    async def command00(self, ctx):
        print("command 00")

    @commands.command()
    async def command01(self, ctx):
        print("command 01")

    @commands.command()
    async def command02(self, ctx):
        print("command 02")

    @commands.command()
    async def command03(self, ctx):
        print("command 03")

    @commands.command()
    async def command04(self, ctx):
        print("command 04")

    @commands.command()
    async def command05(self, ctx):
        print("command 05")

    @commands.command()
    async def command06(self, ctx):
        print("command 06")

    @commands.command()
    async def command07(self, ctx):
        print("command 07")

    @commands.command()
    async def command08(self, ctx):
        print("command 08")

    @commands.command()
    async def command09(self, ctx):
        print("command 09")

    @commands.command()
    async def command10(self, ctx):
        print("command 10")

    @commands.command()
    async def command11(self, ctx):
        print("command 11")

    @commands.command()
    async def command12(self, ctx):
        print("command 12")

    @commands.command()
    async def command13(self, ctx):
        print("command 13")

    @commands.command()
    async def command14(self, ctx):
        print("command 14")

    @commands.command()
    async def command15(self, ctx):
        print("command 15")

    @commands.command()
    async def command16(self, ctx):
        print("command 16")

    @commands.command()
    async def command17(self, ctx):
        print("command 17")

    @commands.command()
    async def command18(self, ctx):
        print("command 18")

    @commands.command()
    async def command19(self, ctx):
        print("command 19")

    @commands.command()
    async def command20(self, ctx):
        print("command 20")

    @commands.command()
    async def command21(self, ctx):
        print("command 21")

    @commands.command()
    async def command22(self, ctx):
        print("command 22")

    @commands.command()
    async def command23(self, ctx):
        print("command 23")

    @commands.command()
    async def command24(self, ctx):
        print("command 24")

    @commands.command()
    async def command25(self, ctx):
        print("command 25")

    @commands.command()
    async def command26(self, ctx):
        print("command 26")

    @commands.command()
    async def command27(self, ctx):
        print("command 27")

    @commands.command()
    async def command28(self, ctx):
        print("command 28")

    @commands.command()
    async def command29(self, ctx):
        print("command 29")


@bot.command()
async def test(ctx: commands.Context):
    await ctx.send("this is the test command")


@commands.cooldown(1, 60)
@bot.command()
async def cooldown_command(ctx: commands.Context):
    cooldown: commands.Cooldown = ctx.command._buckets._cooldown
    print(cooldown.per, cooldown.rate)
    await ctx.send("This command has a cooldown")


def run():
    bot.add_cog(TestCog(bot))
    bot.add_cog(ACog(bot))
    bot.add_cog(LargeCog(bot))
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    run()
