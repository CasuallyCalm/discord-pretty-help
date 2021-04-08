__all__ = ["DefaultMenu", "PrettyMenu"]

import asyncio
import re
from abc import ABCMeta
from typing import List

import discord
from discord.ext import commands


class PrettyMenu(metaclass=ABCMeta):
    """
    A base class for menus used with PrettyHelp
    """

    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):
        """The function called by :class:`PrettyHelp` that will send pages"""
        pass


class DefaultMenu(PrettyMenu):
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
        page_left (str, optional): The emoji to use for going left. Defaults to "◀".
        page_right (str, optional): The emoji to use for going right. Defaults to "▶".
        remove (str, optional): The emoji to use for removing the help message. Defaults to "❌".
    """

    def __init__(
        self, page_left="◀", page_right="▶", remove="❌", active_time=30
    ) -> None:

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
        return f"<Navigation left:{self.page_left} right:{self.page_right} remove:{self.remove}>"

    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):
        total = len(pages)
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

                    try:
                        await message.remove_reaction(
                            payload.emoji, discord.Object(id=payload.user_id)
                        )
                    except discord.errors.Forbidden:
                        pass

                except asyncio.TimeoutError:
                    navigating = False
                    for emoji in self:
                        try:
                            await message.remove_reaction(emoji, bot.user)
                        except Exception:
                            pass
