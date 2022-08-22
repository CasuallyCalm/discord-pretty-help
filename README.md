![version](https://img.shields.io/pypi/v/discord-pretty-help) ![python](https://img.shields.io/badge/python-3.6+-blue)

# discord-pretty-help

An embed version of the built in help command for discord.py



Inspired by the DefaultHelpCommand that discord.py uses, but revised for embeds and additional sorting on individual pages that can be "scrolled" through with reactions.

## Installation

`pip install discord-pretty-help`

## Usage

Example of how to use it:

```python
from discord.ext import commands
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())
```



### Added Optional Args

- `color` - Set the default embed color
- `ending_note` - Set the footer of the embed. Ending notes are fed a `commands.Context` (`ctx`) and a `PrettyHelp` (`help`) instance for more advanced customization.
- `index_title` - Set the index page name default is *"Categories"*
- `menu` - set a custom menu for navigating pages. Uses a `pretty_help.PrettyMenu()` instance. Default is `pretty_help.AppMenu()`
- `no_category` - Set the name of the page with commands not part of a category. Default is "*No Category*"
- `sort_commands` - Sort commands and categories alphabetically
- `show_index` - Show the index page or not

## Menus

### pretty_help.EmojiMenu args

- `active_time` - Set the time (in seconds) that the message will be active. Default is 30s
- `delete_after_timeout` - Delete the message after `active_time` instead of removing reactions. Default `False`
- `page_left` - The emoji to use to page left
- `page_right` - The emoji to use to page right
- `remove` - The emoji to use to remove the help message

### pretty_help.AppMenu
- Uses Application Interactions for navigating

By default, the help will just pick a random color on every invoke. You can change this using the `color` argument:

```python

from discord.ext import commands
from pretty_help import EmojiMenu, PrettyHelp

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
menu = EmojiMenu(page_left="\U0001F44D", page_right="👎", remove=":discord:743511195197374563", active_time=5)

# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

bot = commands.Bot(command_prefix="!")

bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)
```

The basic `help` command will break commands up by cogs. Each cog will be a different page. Those pages can be navigated with
the arrow embeds. The message is unresponsive after 30s of no activity, it'll remove the reactions to let you know.

![example](https://raw.githubusercontent.com/stroupbslayen/discord-pretty-help/master/images/example.gif)


# Changelog

## [2.0.0]
 - Subcommands in pages are indicated with a 🔗, previously it was unclear they were sub commands of the page title



# Notes:
- discord.py must already be installed to use this
- `manage-messages` permission is recommended so reactions can be removed automatically

## Forks for other discord.py based libraries:
* [nextcord-pretty-help](https://github.com/squigjess/nextcord-pretty-help)