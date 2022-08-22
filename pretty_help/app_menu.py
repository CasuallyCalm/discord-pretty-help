from typing import List

import discord
from discord.ext import commands
from discord.ui import Button, Select, View

from .abc_menu import PrettyMenu


class AppMenu(PrettyMenu):
    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):
        ...
