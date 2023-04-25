__all__ = ["PrettyMenu"]

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
