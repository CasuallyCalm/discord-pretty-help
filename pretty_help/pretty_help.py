__all__ = ["PrettyHelp"]

import asyncio
from random import randint, uniform
from typing import List, Union

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.help import HelpCommand

from .navigation import Navigation


class Paginator:
    """A class that aids in paginating code blocks for Discord messages.
    .. container:: operations
        .. describe:: len(x)
            Returns the total number of characters in the paginator.
    Attributes
    -----------
    prefix: Optional[:class:`str`]
        The prefix inserted to every page. e.g. three backticks.
    suffix: Optional[:class:`str`]
        The suffix appended at the end of every page. e.g. three backticks.
    max_size: :class:`int`
        The maximum amount of codepoints allowed in a page.
    navigation: :class:`pretty_help.Navigation`
        Sets the emojis that conrol the help menu
    color: Optional[:class:`discord.Color`, :class: `int`]
        The color of the disord embed. Default is a random color for every invoke
    ending_note: Optional[:class:`str`]
        The footer in of the help embed
    """

    def __init__(self, color=0):
        self.ending_note = None
        self.color = color
        self.char_limit = 6000
        self.field_limit = 25
        self.prefix = "```"
        self.suffix = "```"
        self.clear()

    def clear(self):
        """Clears the paginator to have no pages."""
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        """
        Check if the emebed is too big to be sent on discord

        Args:
            embed (discord.Embed): The embed to check

        Returns:
            bool: Will return True if the emebed isn't too large
        """
        check = (
            len(embed) + sum(len(char) for char in chars if char) < self.char_limit
            and len(embed.fields) < self.field_limit
        )
        return check

    def _new_page(self, title: str, description: str):
        """
        Create a new page

        Args:
            title (str): The title of the new page

        Returns:
            discord.Emebed: Returns an embed with the title and color set
        """
        return discord.Embed(title=title, description=description, color=self.color)

    def _add_page(self, page: discord.Embed):
        """
        Add a page to the paginator

        Args:
            page (discord.Embed): The page to add
        """
        page.set_footer(text=self.ending_note)
        self._pages.append(page)

    def add_cog(
        self, title: Union[str, commands.Cog], commands_list: List[commands.Command]
    ):
        """
        Add a cog page to the help menu

        Args:
            title (Union[str, commands.Cog]): The title of the embed
            commands_list (List[commands.Command]): List of commands
        """
        cog = isinstance(title, commands.Cog)
        if not commands_list:
            return

        page_title = title.qualified_name if cog else title
        embed = self._new_page(page_title, (title.description or "") if cog else "")

        self._add_command_fields(embed, page_title, commands_list)

    def _add_command_fields(
        self, embed: discord.Embed, page_title: str, commands: List[commands.Command]
    ):
        """
        Adds command fields to Category/Cog and Command Group pages

        Args:
            embed (discord.Embed): The page to add command descriptions
            page_title (str): The title of the page
            commands (List[commands.Command]): The list of commands for the fields
        """
        for command in commands:
            if not self._check_embed(
                embed,
                self.ending_note,
                command.name,
                command.short_doc,
                self.prefix,
                self.suffix,
            ):
                self._add_page(embed)
                embed = self._new_page(page_title, embed.description)

            embed.add_field(
                name=command.name,
                value=f'{self.prefix}{command.short_doc or "No Description"}{self.suffix}',
                inline=False,
            )
        self._add_page(embed)

    @staticmethod
    def __command_info(command: Union[commands.Command, commands.Group]):
        info = ""
        if command.description:
            info += command.description + "\n\n"
        if command.help:
            info += command.help
        if not info:
            info = "None"
        return info

    def add_command(self, command: commands.Command, signature: str):
        """
        Add a command help page

        Args:
            command (commands.Command): The command to get help for
            signature (str): The command signature/usage string
        """
        desc = f"{command.description}\n\n" if command.description else ""
        page = self._new_page(
            command.qualified_name,
            f"{self.prefix}{self.__command_info(command)}{self.suffix}" or "",
        )
        if command.aliases:
            aliases = ", ".join(command.aliases)
            page.add_field(
                name="Aliases",
                value=f"{self.prefix}{aliases}{self.suffix}",
                inline=False,
            )
        page.add_field(
            name="Usage", value=f"{self.prefix}{signature}{self.suffix}", inline=False
        )
        self._add_page(page)

    def add_group(self, group: commands.Group, commands_list: List[commands.Command]):
        """
        Add a group help page

        Args:
            group (commands.Group): The command group to get help for
            commands_list (List[commands.Command]): The list of commands in the group
        """
        page = self._new_page(
            group.name, f"{self.prefix}{self.__command_info(group)}{self.suffix}" or ""
        )

        self._add_command_fields(page, group.name, commands_list)

    def add_index(self, include: bool, title: str, bot: commands.Bot):
        """
        Add an index page to the response of the bot_help command

        Args:
            include (bool): Include the index page or not
            title (str): The title of the index page
            bot (commands.Bot): The bot instance
        """
        if include:
            index = self._new_page(title, bot.description or "")

            for page_no, page in enumerate(self._pages, 2):
                index.add_field(
                    name=f"{page_no}) {page.title}",
                    value=f'{self.prefix}{page.description or "No Description"}{self.suffix}',
                    inline=False,
                )
            index.set_footer(text=self.ending_note)
            self._pages.insert(0, index)
        else:
            self._pages[0].description = bot.description

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        if len(self._pages) == 1:
            return self._pages
        lst = []
        for page_no, page in enumerate(self._pages, start=1):
            page: discord.Embed
            page.description = (
                f"`Page: {page_no}/{len(self._pages)}`\n{page.description}"
            )
            lst.append(page)
        return lst


class PrettyHelp(HelpCommand):
    """The implementation of the prettier help command.
    A more refined help command format
    This inherits from :class:`HelpCommand`.
    It extends it with the following attributes.

    Attributes
    ------------

    active_time: :class: `int`
        The time in seconds the message will be active for. Default is 10.
    color: :class: `discord.Color`
        The color to use for the help embeds. Default is a random color.
    dm_help: Optional[:class:`bool`]
        A tribool that indicates if the help command should DM the user instead of
        sending it to the channel it received it from. If the boolean is set to
        ``True``, then all help output is DM'd. If ``False``, none of the help
        output is DM'd. If ``None``, then the bot will only DM when the help
        message becomes too long (dictated by more than :attr:`dm_help_threshold` characters).
        Defaults to ``False``.
    ending_note: Optional[:class:`str`]
        The footer in of the help embed
    index_title: :class: `str`
        The string used when the index page is shown. Defaults to ``"Categories"``
    navigation: Optional[:class:`pretty_help.Navigation`]
        Sets the emojis that conrol the help menu
    no_category: :class:`str`
        The string used when there is a command which does not belong to any category(cog).
        Useful for i18n. Defaults to ``"No Category"``
    sort_commands: :class:`bool`
        Whether to sort the commands in the output alphabetically. Defaults to ``True``.
    show_index: class: `bool`
        A bool that indicates if the index page should be shown listing the available cogs
        Defaults to ``True``.

    """

    def __init__(self, **options):

        self.active_time = options.pop("active_time", 30)
        self.color = options.pop(
            "color",
            discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        self.dm_help = options.pop("dm_help", False)
        self.index_title = options.pop("index_title", "Categories")
        self.navigation = options.pop("navigation", Navigation())
        self.no_category = options.pop("no_category", "No Category")
        self.sort_commands = options.pop("sort_commands", True)
        self.show_index = options.pop("show_index", True)
        self.paginator = Paginator(color=self.color)
        self.ending_note = options.pop("ending_note", "")

        super().__init__(**options)

    async def prepare_help_command(
        self, ctx: commands.Context, command: commands.Command
    ):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.guild.me)
            if not perms.embed_links:
                raise commands.BotMissingPermissions(("embed links",))
            if not perms.read_message_history:
                raise commands.BotMissingPermissions(("read message history",))
            if not perms.add_reactions:
                raise commands.BotMissingPermissions(("add reactions permission",))

        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    def get_ending_note(self):
        """Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        return self.ending_note or (
            "Type {0}{1} command for more info on a command.\n"
            "You can also type {0}{1} category for more info on a category.".format(
                self.clean_prefix, command_name
            )
        )

    async def send_pages(self):
        """A helper utility to send the page output from :attr:`paginator` to the destination."""

        pages = self.paginator.pages
        total = len(pages)
        destination = self.get_destination()

        message: discord.Message = await destination.send(embed=pages[0])

        if total > 1:
            bot: commands.Bot = self.context.bot
            navigating = True
            index = 0

            for reaction in self.navigation:
                await message.add_reaction(reaction)

            while navigating:
                try:

                    def check(payload: discord.RawReactionActionEvent):

                        if (
                            payload.user_id != bot.user.id
                            and message.id == payload.message_id
                        ):
                            return True

                    payload: discord.RawReactionActionEvent = await bot.wait_for(
                        "raw_reaction_add", timeout=self.active_time, check=check
                    )

                    emoji_name = (
                        payload.emoji.name
                        if payload.emoji.id is None
                        else f":{payload.emoji.name}:{payload.emoji.id}"
                    )

                    if (
                        emoji_name in self.navigation
                        and payload.user_id == self.context.author.id
                    ):
                        nav = self.navigation.get(emoji_name)
                        if not nav:

                            navigating = False
                            return await message.delete()
                        else:
                            index += nav
                            embed: discord.Embed = pages[index % total]

                            await message.edit(embed=embed)

                    try:
                        await message.remove_reaction(
                            payload.emoji, discord.Object(id=payload.user_id)
                        )
                    except discord.errors.Forbidden:
                        pass

                except asyncio.TimeoutError:
                    navigating = False
                    for emoji in self.navigation:
                        try:
                            await message.remove_reaction(emoji, bot.user)
                        except Exception:
                            pass

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        else:
            return ctx.channel

    async def send_bot_help(self, mapping: dict):
        bot = self.context.bot
        channel = self.get_destination()
        async with channel.typing():
            mapping = dict((name, []) for name in mapping)
            help_filtered = (
                filter(lambda c: c.name != "help", bot.commands)
                if len(bot.commands) > 1
                else bot.commands
            )
            for cmd in await self.filter_commands(
                help_filtered,
                sort=self.sort_commands,
            ):
                mapping[cmd.cog].append(cmd)
            self.paginator.add_cog(self.no_category, mapping.pop(None))
            sorted_map = sorted(
                mapping.items(),
                key=lambda cg: cg[0].qualified_name
                if isinstance(cg[0], commands.Cog)
                else str(cg[0]),
            )
            for cog, command_list in sorted_map:
                self.paginator.add_cog(cog, command_list)
            self.paginator.add_index(self.show_index, self.index_title, bot)
        await self.send_pages()

    async def send_command_help(self, command: commands.Command):
        filtered = await self.filter_commands([command])
        if filtered:
            self.paginator.add_command(command, self.get_command_signature(command))
            await self.send_pages()

    async def send_group_help(self, group: commands.Group):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                group.commands, sort=self.sort_commands
            )
            # if filtered:
            self.paginator.add_group(group, filtered)
        await self.send_pages()

    async def send_cog_help(self, cog: commands.Cog):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                cog.get_commands(), sort=self.sort_commands
            )
            self.paginator.add_cog(cog, filtered)
        await self.send_pages()
