__all__ = ["AppMenu"]

from typing import List, Optional

import discord
from discord.ext import commands
from discord.ui import Button, Select, View

from .abc_menu import PrettyMenu


class HelpNav(View):

    index = 0

    def __init__(self, pages: List[discord.Embed], timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.page_count = len(pages)
        self.pages = pages

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.success)
    async def previous(self, interaction: discord.Interaction, button: Button):
        self.index -= 1
        await self.update(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):
        self.index += 1
        await self.update(interaction)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def _delete(self, interaction: discord.Interaction, button: Button):
        await interaction.message.delete()

    async def update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=self.pages[self.index % self.page_count]
        )


class AppMenu(PrettyMenu):
    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):
        await ctx.send(embed=pages[0], view=HelpNav(pages))
