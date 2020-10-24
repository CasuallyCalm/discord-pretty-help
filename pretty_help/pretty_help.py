__all__ = ["PrettyHelp"]

import asyncio
import itertools
from random import randint

import discord
from discord.ext import commands
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
    """

    def __init__(
        self,
        navigation: Navigation,
        color=None,
        prefix="```",
        suffix="```",
        max_size=2000,
    ):
        self.navigation = navigation
        self.ending_note = None
        self.prefix = prefix
        self.suffix = suffix
        self.max_size = max_size - (0 if suffix is None else len(suffix))
        self.color = (
            color
            if color
            else discord.Color.from_rgb(
                randint(0, 255), randint(0, 255), randint(0, 255)
            )
        )
        self.clear()

    def clear(self):
        """Clears the paginator to have no pages."""
        self._current_page = 0
        self._pages = []

    def get_page_reaction(self, emoji):
        """Returns the current page based on an emoji"""
        nav = self.navigation.get(emoji)
        if nav:
            pages = len(self._pages) - 1
            self._current_page += nav
            if self._current_page < 0:
                self._current_page = pages
            if self._current_page > pages:
                self._current_page = 0
            return self._current_page

    @property
    def _prefix_len(self):
        return len(self.prefix) if self.prefix else 0

    def add_page(self, page_name):
        """Adds a page"""
        embed = discord.Embed(
            title=page_name, description=self.prefix, color=self.color
        )
        embed.set_footer(text=self.ending_note)
        self._pages.append(embed)
        return embed

    def get_page_index(self, page_index: int):
        "Gets the page based on it's index value"
        embed = self._pages[page_index]
        if not embed.description.startswith("`Page:"):
            embed.description = (
                f"`Page:{page_index+1}/{len(self._pages)}`\n{embed.description}"
            )
        return embed

    def get_page(self, page_name, line=""):
        """Gets a page based on its title."""
        for page in self._pages:
            if page.title == page_name and (len(page) + len(line) + 1 < self.max_size):
                return page
        return self.add_page(page_name)

    def add_line(self, page_name, line="", *, empty=False):
        """Adds a line to the current page.
        If the line exceeds the :attr:`max_size` then an exception
        is raised.
        Parameters
        -----------
        line: :class:`str`
            The line to add.
        empty: :class:`bool`
            Indicates if another empty line should be added.
        Raises
        ------
        RuntimeError
            The line was too big for the current :attr:`max_size`.
        """
        page = self.get_page(page_name, line)

        max_page_size = self.max_size - self._prefix_len - 2
        if len(line) > max_page_size:
            raise RuntimeError("Line exceeds maximum page size %s" % (max_page_size))

        page.description += line + "\n"

        if empty:
            page.description += "\n"

    def __len__(self):
        total = sum(len(p) for p in self._pages)
        return total + self._count

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        # we have more than just the prefix in our current page
        return self._pages

    def __repr__(self):
        fmt = "<Paginator prefix: {0.prefix} suffix: {0.suffix} max_size: {0.max_size} count: {0._count}>"
        return fmt.format(self)


class PrettyHelp(HelpCommand):
    """The implementation of the prettier help command.
    Basically a prettier DefaultHelpCommand
    This inherits from :class:`HelpCommand`.
    It extends it with the following attributes.
    Attributes
    ------------
    width: :class:`int`
        The maximum number of characters that fit in a line.
        Defaults to 80.
    sort_commands: :class:`bool`
        Whether to sort the commands in the output alphabetically. Defaults to ``True``.
    dm_help: Optional[:class:`bool`]
        A tribool that indicates if the help command should DM the user instead of
        sending it to the channel it received it from. If the boolean is set to
        ``True``, then all help output is DM'd. If ``False``, none of the help
        output is DM'd. If ``None``, then the bot will only DM when the help
        message becomes too long (dictated by more than :attr:`dm_help_threshold` characters).
        Defaults to ``False``.
    dm_help_threshold: Optional[:class:`int`]
        The number of characters the paginator must accumulate before getting DM'd to the
        user if :attr:`dm_help` is set to ``None``. Defaults to 1000.
    indent: :class:`int`
        How much to intend the commands from a heading. Defaults to ``2``.
    commands_heading: :class:`str`
        The command list's heading string used when the help command is invoked with a category name.
        Useful for i18n. Defaults to ``"Commands:"``
    navigation: Optional[:class:`pretty_help.Navigation`]
        Sets the emojis that conrol the help menu
    no_category: :class:`str`
        The string used when there is a command which does not belong to any category(cog).
        Useful for i18n. Defaults to ``"No Category"``
    paginator: :class:`Paginator`
        The paginator used to paginate the help command output.
    color: :class: `discord.Color`
        The color to use for the help embeds. Default is a random color.
    active: :class: `int`
        The time in seconds the message will be active for. Default is 10.
    show_index: class: `bool`
        A bool that indicates if the index page should be shown listing the available cogs
        Defaults to ``True``.
    index: :class: `str`
        The string used when the index page is shown. Defaults to ``"Categories"``
    """

    def __init__(self, **options):
        self.width = options.pop("width", 58)
        self.indent = options.pop("indent", 2)
        self.sort_commands = options.pop("sort_commands", True)
        self.dm_help = options.pop("dm_help", False)
        self.dm_help_threshold = options.pop("dm_help_threshold", 1000)
        self.commands_heading = options.pop("commands_heading", "Commands:")
        self.no_category = options.pop("no_category", "No Category")
        self.paginator = options.pop("paginator", None)
        self.active = options.pop("active", 30)
        self.navigation = options.pop("navigation", Navigation())
        self.show_index = options.pop("show_index", True)
        self.index = options.pop("index", "Categories")
        self.paginator = self.paginator or Paginator(
            self.navigation, color=options.pop("color", None)
        )

        super().__init__(**options)

    def shorten_text(self, text):
        """Shortens text to fit into the :attr:`width`."""
        if len(text) > self.width:
            return text[: self.width - 3] + "..."
        return text

    def get_ending_note(self):
        """Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        return (
            "Type {0}{1} command for more info on a command.\n"
            "You can also type {0}{1} category for more info on a category.".format(
                self.clean_prefix, command_name
            )
        )

    def add_indented_commands(self, commands, *, heading, max_size=None, group=None):
        """Indents a list of commands after the specified heading.
        The formatting is added to the :attr:`paginator`.
        The default implementation is the command name indented by
        :attr:`indent` spaces, padded to ``max_size`` followed by
        the command's :attr:`Command.short_doc` and then shortened
        to fit into the :attr:`width`.
        Parameters
        -----------
        commands: Sequence[:class:`Command`]
            A list of commands to indent for output.
        heading: :class:`str`
            The heading to add to the output. This is only added
            if the list of commands is greater than 0.
        max_size: Optional[:class:`int`]
            The max size to use for the gap between indents.
            If unspecified, calls :meth:`get_max_size` on the
            commands parameter.
        """

        if not commands:
            return

        # self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)
        if group:
            self.paginator.add_line(group.name, heading)
        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = "{0}{1:<{width}} {2}".format(
                self.indent * " ", name, command.short_doc, width=width
            )
            if group:
                self.paginator.add_line(group.name, self.shorten_text(entry))
            else:
                self.paginator.add_line(heading, self.shorten_text(entry))

    async def send_pages(self, bot_help=False):
        """A helper utility to send the page output from :attr:`paginator` to the destination."""
        destination = self.get_destination()
        ctx = self.context
        bot = self.context.bot

        if ctx.guild is not None:
            print("Checking perms")
            perms = ctx.channel.permissions_for(ctx.guild.me)
            if not perms.embed_links:
                raise commands.BotMissingPermissions(("embed links",))
            if not perms.read_message_history:
                raise commands.BotMissingPermissions(("read message history",))
            if not perms.add_reactions:
                raise commands.BotMissingPermissions(("add reactions permission",))

        for page in self.paginator.pages:
            page.description += "```"

        message: discord.Message = await destination.send(
            embed=self.paginator.get_page_index(0)
        )
        if bot_help:

            for emoji in self.navigation:
                await message.add_reaction(emoji)

            while bot_help:
                try:

                    def check(reaction: discord.Reaction, user):

                        if user != bot.user and message.id == reaction.message.id:
                            return True

                    reaction, user = await bot.wait_for(
                        "reaction_add", timeout=self.active, check=check
                    )

                    user_check = user == ctx.author
                    emoji_check = reaction.emoji in self.navigation
                    if emoji_check and user_check:
                        next_page = self.paginator.get_page_reaction(reaction.emoji)
                        if next_page is None:
                            return await message.delete()
                        embed: discord.Embed = self.paginator.get_page_index(next_page)

                        await message.edit(embed=embed)

                    try:
                        await message.remove_reaction(reaction.emoji, user)
                    except discord.errors.Forbidden:
                        pass
                except asyncio.TimeoutError:
                    bot_help = False
                    for emoji in self.navigation:
                        try:
                            await message.remove_reaction(emoji, bot.user)
                        except Exception:
                            pass

    def add_command_formatting(self, command):
        """A utility function to format the non-indented block of commands and groups.
        Parameters
        ------------
        command: :class:`Command`
            The command to format.
        """

        if command.description:
            self.paginator.add_line(command.name, command.description, empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(command.name, signature, empty=True)

        if command.help:
            try:
                self.paginator.add_line(command.name, command.help, empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(command.name, line)
                self.paginator.add_line(command.name)

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        elif self.dm_help is None and len(self.paginator) > self.dm_help_threshold:
            return ctx.author
        else:
            return ctx.channel

    async def prepare_help_command(self, ctx, command):
        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        no_category = self._no_category

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.qualified_name + ":" if cog is not None else no_category

        help_filtered = (
            filter(lambda c: c.name != "help", bot.commands)
            if len(bot.commands) > 1
            else bot.commands
        )

        filtered = await self.filter_commands(
            help_filtered, sort=self.sort_commands, key=get_category
        )

        if self.show_index and bot.cogs:
            if bot.description:
                self.paginator.add_line(self._index, bot.description, empty=True)

            get_width = discord.utils._string_width
            cogs = bot.cogs
            max_size = max(map(len, cogs))
            cog_objects = (
                sorted(cogs.values(), key=lambda c: c.qualified_name)
                if self.sort_commands
                else cogs.values()
            )
            for cog in cog_objects:
                cog_name = cog.qualified_name
                width = max_size - (get_width(cog_name) - len(cog_name))
                description = cog.description if cog.description else ""
                entry = "{0}{1:<{width}}| {2}".format(
                    self.indent * " ", cog_name, description, width=width
                )
                self.paginator.add_line(self._index, self.shorten_text(entry))

            if not all(command.cog for command in filtered):
                self.paginator.add_line(no_category, "", empty=True)

        else:
            if bot.description:
                # <description> portion
                self.paginator.add_line(no_category, bot.description, empty=True)

        max_size = self.get_max_size(filtered)
        to_iterate = itertools.groupby(filtered, key=get_category)

        # Now we can add the commands to the page.
        for category, commands in to_iterate:
            commands = (
                sorted(commands, key=lambda c: c.name)
                if self.sort_commands
                else list(commands)
            )
            self.add_indented_commands(commands, heading=category, max_size=max_size)

        await self.send_pages(bot_help=True)

    @property
    def _no_category(self):
        return "{0.no_category}:".format(self)

    @property
    def _index(self):
        return "{0.index}:".format(self)

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        await self.send_pages()

    async def send_group_help(self, group):
        self.add_command_formatting(group)

        filtered = await self.filter_commands(group.commands, sort=self.sort_commands)
        self.add_indented_commands(filtered, heading=self.commands_heading, group=group)

        if filtered:
            self.paginator.add_line(group.name)

        await self.send_pages()

    async def send_cog_help(self, cog):
        if cog.description:
            self.paginator.add_line(cog.qualified_name, f"{cog.description}\n")

        filtered = await self.filter_commands(
            cog.get_commands(), sort=self.sort_commands
        )
        self.add_indented_commands(filtered, heading=cog.qualified_name)
        self.paginator.add_line(cog.qualified_name)

        await self.send_pages()
