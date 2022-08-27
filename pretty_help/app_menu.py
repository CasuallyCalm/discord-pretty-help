__all__ = ["AppMenu", "AppNav"]

from optparse import Option
from typing import List, Optional

import discord
from discord.ext import commands
from discord.ui import Button, Select, View

from .abc_menu import PrettyMenu


class AppNav(View):
    """
    The acutal View for controlling the menu interaction

    Args:
        pages (List[discord.Embed], optional): List of pages the cycle through. Defaults to None.
        timeout (Optional[float], optional): The duration the interaction will be active for. Defaults to None.
        ephemeral (Optional[bool], optional): Send as an ephemeral message. Defaults to False.
    """

    index = 0

    def __init__(
        self,
        pages: List[discord.Embed] = None,
        timeout: Optional[float] = None,
        ephemeral: Optional[bool] = False,
    ):
        super().__init__(timeout=timeout)
        self.page_count = len(pages) if pages else None
        self.pages = pages

        if pages and len(pages) == 1:
            self.remove_item(self.previous)
            self.remove_item(self.next)
            self.remove_item(self.select)

        if ephemeral:
            self.remove_item(self._delete)

        if pages and len(pages) > 1:
            for index, page in enumerate(pages):
                self.select.add_option(
                    label=f"{page.title}",
                    description=page.description.replace("`",""),
                    value=index,
                )

    @discord.ui.button(
        label="Previous",
        style=discord.ButtonStyle.success,
        row=1,
        custom_id="pretty_help:previous",
    )
    async def previous(self, interaction: discord.Interaction, button: Button):
        self.index -= 1
        await self.update(interaction)

    @discord.ui.button(
        label="Next",
        style=discord.ButtonStyle.primary,
        row=1,
        custom_id="pretty_help:next",
    )
    async def next(self, interaction: discord.Interaction, button: Button):
        self.index += 1
        await self.update(interaction)

    @discord.ui.button(
        label="Delete",
        style=discord.ButtonStyle.danger,
        row=1,
        custom_id="pretty_help:delete",
    )
    async def _delete(self, interaction: discord.Interaction, button: Button):
        await interaction.message.delete()

    @discord.ui.select(row=2, custom_id="pretty_help:select")
    async def select(self, interatcion: discord.Interaction, select: Select):
        self.index = int(select.values[0])
        await self.update(interatcion)

    async def update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=self.pages[self.index % self.page_count], view=self
        )


class AppMenu(PrettyMenu):
    """
    Navigate pages using the Discord UI components.

    This menu can be *partially* persistant with 'client.add_view(AppMenu())`
    This will allow the delete button to work on past messages

    Args:
        timeout (Optional[float], optional): The duration the interaction will be active for. Defaults to None.
        ephemeral (Optional[bool], optional): Send as an ephemeral message. Defaults to False.
    """

    def __init__(
        self,
        timeout: Optional[float] = None,
        ephemeral: Optional[bool] = False,
    ) -> None:
        # super().__init__()
        self.timeout = timeout
        self.ephemeral = ephemeral

    async def send_pages(
        self,
        ctx: commands.Context,
        destination: discord.abc.Messageable,
        pages: List[discord.Embed],
    ):

        if ctx.interaction:
            await ctx.interaction.response.send_message(
                embed=pages[0],
                view=AppNav(
                    pages=pages, timeout=self.timeout, ephemeral=self.ephemeral
                ),
                ephemeral=self.ephemeral,
            )
        else:
            await destination.send(
                embed=pages[0], view=AppNav(pages=pages, timeout=self.timeout)
            )
