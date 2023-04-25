import contextlib

__all__ = ["EmojiMenu"]

import asyncio
import re
from typing import List

import discord
from discord.ext import commands

from .abc_menu import PrettyMenu


class EmojiMenu(PrettyMenu):
    """The default navigation menu for PrettyHelp.

    Accepts standard emojis in multiple ways:
        - Emoji:: "👍"
        - Unicode:: "\\U0001F44D"
        - Unicode Name:: "\\N{THUMBS UP SIGN}"

    Using a custom emoji:
        - Discord emoji id:: ":custom_emoji:8675309"

    Use `\` to get the discord representation:
        Example: '\\\:custom_emoji:' in discord

    Args:
        active_time: :class: `int`
            The time in seconds the menu will be active for. Default is 10.
        delete_after_timeout: :class: `bool`
            Delete the message after `active_time` instead of removing reactions.
        page_left (str, optional): The emoji to use for going left. Defaults to "◀".
        page_right (str, optional): The emoji to use for going right. Defaults to "▶".
        remove (str, optional): The emoji to use for removing the help message. Defaults to "❌".
    """

    def __init__(
        self,
        page_left="◀",
        page_right="▶",
        remove="❌",
        active_time=30,
        delete_after_timeout=False,
    ) -> None:
        self.delete_after_timeout = delete_after_timeout
        self.page_left = self.__match(page_left)
        self.page_right = self.__match(page_right)
        self.remove = self.__match(remove)
        self.active_time = active_time

    @property
    def _dict(self) -> dict:
        return {
            self.page_left: -1,
            self.page_right: 1,
            self.remove: 0,
        }

    @staticmethod
    def custom(emoji):
        return f":{emoji.name}:{emoji.id}"

    def get(self, emoji):
        if isinstance(emoji, str):
            return self._dict.get(emoji)
        else:
            return self._dict.get(self.custom(emoji))

    def __contains__(self, emoji):
        if isinstance(emoji, str):
            return emoji in self._dict
        else:
            return self.custom(emoji) in self._dict

    @staticmethod
    def __match(emoji: str):
        try:
            pattern = r":[a-zA-Z0-9]+:[0-9]+"
            return re.search(pattern=pattern, string=emoji)[0]
        except TypeError:
            return emoji

    def __iter__(self):
        return self._dict.__iter__()

    def __repr__(self) -> str:
        return f"<EmojiMenu left:{self.page_left} right:{self.page_right} remove:{self.remove}>"

    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):
        total = len(pages)

        # this is a quick way to make the emoji menu appear to work correctly when called as an app command
        # otherwise the interaction will error
        if ctx.interaction:
            await ctx.interaction.response.defer()
            await ctx.interaction.delete_original_response()

        message: discord.Message = await destination.send(embed=pages[0])

        if total > 1:
            bot: commands.Bot = ctx.bot
            navigating = True
            index = 0

            for reaction in self:
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

                    if emoji_name in self and payload.user_id == ctx.author.id:
                        nav = self.get(emoji_name)
                        if not nav:

                            navigating = False
                            return await message.delete()
                        else:
                            index += nav
                            embed: discord.Embed = pages[index % total]

                            await message.edit(embed=embed)

                    with contextlib.suppress(discord.errors.Forbidden):
                        await message.remove_reaction(
                            payload.emoji, discord.Object(id=payload.user_id)
                        )

                except asyncio.TimeoutError:
                    navigating = False
                    if self.delete_after_timeout:
                        await message.delete()
                    else:
                        for emoji in self:
                            with contextlib.suppress(Exception):
                                await message.remove_reaction(emoji, bot.user)
