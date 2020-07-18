![version](https://img.shields.io/pypi/v/discord-pretty-help) ![python](https://img.shields.io/badge/python-3.6+-blue)

# discord-pretty-help

An embed version of the built in help command for discord.py

Based on the DefaultHelpCommand that discord.py uses, but revised for embeds and cogs on individual pages that can be "scrolled" through with reactions.

## Installation

`pip install discord-pretty-help`

## Usage

Example of how to use it:

```python
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())
```

### Optional Args

- `color` - Set the default embed color
- `active` - Set the time (in seconds) that the message will be active default is 30s

By default, the help will just pick a random color on every invoke. You can change this using the `color` argument:

```python
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp(color=discord.Color.dark_gold(), active=5)) #message will be active for 5s
```

The basic `help` command will break commands up by cogs. Each cog will be a different page. Those pages can be navigated with
the arrow embeds. The message is unresponsive after 30s of no activity, it'll remove the reactions to let you know.

![example](https://raw.githubusercontent.com/stroupbslayen/discord-pretty-help/master/images/example.gif)

## Notes:

- discord.py must already be installed to use this
- `manage-messages` permission is recommended so reactions can be removed automatically
