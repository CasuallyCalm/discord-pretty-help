"""
Note: Rename `env.example` to `.env` and enter your token then run `poetry run test` in your terminal
"""
import os

import discord
import dotenv
from discord import app_commands
from discord.ext import commands
from pretty_help import EmojiMenu, PrettyHelp

dotenv.load_dotenv("./tests/.env")

# for testing standard text based commands, ie !ping, make sure the message content intent ON in the discord bot app page
intents = discord.Intents.default()
intents.message_content = True

MY_GUILD = discord.Object(id=os.environ.get("GUILD_ID"))


# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"


bot = commands.Bot(
    command_prefix="!",
    description="this is the bots descripton",
    intents=intents,
    help_command=PrettyHelp(ending_note=ending_note),
)


def use_emoji_menu():
    # ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
    menu = EmojiMenu(
        "\U0001F44D",
        "👎",
        ":discord:743511195197374563",
        active_time=60,
        delete_after_timeout=False,
    )
    bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)


####### Text command Stuff
class TextCommandCog(commands.Cog):
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


class TextGroupCog(commands.Cog, name="Z Cog"):
    """This is a cog for testing purposes"""

    @commands.group(description="This is a group description")
    async def groupCommand1(self, ctx: commands.Context):
        """This is group help"""
        await ctx.send("This is a test command")

    @groupCommand1.command()
    async def subCommand1(self, ctx: commands.Context):
        await ctx.send("this is a subcommand")


class LargeTextCommandCog(commands.Cog):
    @commands.command()
    async def command00(self, ctx: commands.Context):
        print("command 00")

    @commands.command()
    async def command01(self, ctx: commands.Context):
        print("command 01")

    @commands.command()
    async def command02(self, ctx: commands.Context):
        print("command 02")

    @commands.command()
    async def command03(self, ctx: commands.Context):
        print("command 03")

    @commands.command()
    async def command04(self, ctx: commands.Context):
        print("command 04")

    @commands.command()
    async def command05(self, ctx: commands.Context):
        print("command 05")

    @commands.command()
    async def command06(self, ctx: commands.Context):
        print("command 06")

    @commands.command()
    async def command07(self, ctx: commands.Context):
        print("command 07")

    @commands.command()
    async def command08(self, ctx: commands.Context):
        print("command 08")

    @commands.command()
    async def command09(self, ctx: commands.Context):
        print("command 09")

    @commands.command()
    async def command10(self, ctx: commands.Context):
        print("command 10")

    @commands.command()
    async def command11(self, ctx: commands.Context):
        print("command 11")

    @commands.command()
    async def command12(self, ctx: commands.Context):
        print("command 12")

    @commands.command()
    async def command13(self, ctx: commands.Context):
        print("command 13")

    @commands.command()
    async def command14(self, ctx: commands.Context):
        print("command 14")

    @commands.command()
    async def command15(self, ctx: commands.Context):
        print("command 15")

    @commands.command()
    async def command16(self, ctx: commands.Context):
        print("command 16")

    @commands.command()
    async def command17(self, ctx: commands.Context):
        print("command 17")

    @commands.command()
    async def command18(self, ctx: commands.Context):
        print("command 18")

    @commands.command()
    async def command19(self, ctx: commands.Context):
        print("command 19")

    @commands.command()
    async def command20(self, ctx: commands.Context):
        print("command 20")

    @commands.command()
    async def command21(self, ctx: commands.Context):
        print("command 21")

    @commands.command()
    async def command22(self, ctx: commands.Context):
        print("command 22")

    @commands.command()
    async def command23(self, ctx: commands.Context):
        print("command 23")

    @commands.command()
    async def command24(self, ctx: commands.Context):
        print("command 24")

    @commands.command()
    async def command25(self, ctx: commands.Context):
        print("command 25")

    @commands.command()
    async def command26(self, ctx: commands.Context):
        print("command 26")

    @commands.command()
    async def command27(self, ctx: commands.Context):
        print("command 27")

    @commands.command()
    async def command28(self, ctx: commands.Context):
        print("command 28")

    @commands.command()
    async def command29(self, ctx: commands.Context):
        print("command 29")


####### App Command stuff
class AppCommandCog(commands.Cog):
    """And Cog with app commands and a message command"""

    @commands.command()
    async def text_command(self, ctx: commands.Context):
        """normal message command with app commands"""
        await ctx.send("normal message command with app commands")

    @app_commands.command()
    async def _app_command(self, interaction: discord.Interaction):
        """This is an app command description"""
        await interaction.response.send_message("This is an app command")

    @app_commands.command(nsfw=True)
    async def nsfw_app_command(self, interaction: discord.Interaction):
        """This is an app command description and is NSFW"""
        await interaction.response.send_message("This is an app command, also NSFW")

    @app_commands.command()
    @app_commands.describe(message="The message the will be repeated")
    async def repeat(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


class GroupAppCommandCog(commands.GroupCog):
    """A group of app commands in a cog"""

    @app_commands.command()
    async def _app_command(self, interaction: discord.Interaction):
        """This is an app command description"""
        await interaction.response.send_message("This is an app command")

    @app_commands.command(nsfw=True)
    async def nsfw_app_command(self, interaction: discord.Interaction):
        """This is an app command description and is NSFW"""
        await interaction.response.send_message("This is an app command, also NSFW")

    @app_commands.command()
    @app_commands.describe(message="The message the will be repeated")
    async def repeat(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


######## Context Menus


@bot.tree.context_menu(nsfw=True)
async def nsfw_reply(interaction: discord.Interaction, message: discord.Message):
    await message.reply(f"That's a nice message! - {interaction.user.mention}")


@bot.tree.context_menu(name="reply")
async def reply(interaction: discord.Interaction, message: discord.Message):
    await message.reply(f"That's a nice message! - {interaction.user.mention}")


@bot.tree.context_menu(nsfw=True)
async def nsfw_ban(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"Ban {member.display_name}?", ephemeral=True
    )


@bot.tree.context_menu()
async def ban(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"Ban {member.display_name}?", ephemeral=True
    )


########


@bot.command()
async def test(ctx: commands.Context):
    await ctx.send("this is the test command")


@commands.cooldown(1, 60)
@bot.command()
async def cooldown_command(ctx: commands.Context):
    cooldown: commands.Cooldown = ctx.command._buckets._cooldown
    print(cooldown.per, cooldown.rate)
    await ctx.send("This command has a cooldown")


async def setup():
    await bot.add_cog(TextCommandCog())
    await bot.add_cog(TextGroupCog())
    await bot.add_cog(LargeTextCommandCog())
    await bot.add_cog(AppCommandCog())
    await bot.add_cog(GroupAppCommandCog())
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    print(f"Logged in as: {bot.user.name}")
    print(f"With ID: {bot.user.id}")


bot.setup_hook = setup


def run():
    bot.run(os.environ.get("TOKEN"))


def run_emoji():
    use_emoji_menu()
    run()


if __name__ == "__main__":
    run()
