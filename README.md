# discord-pretty-help

An embed version of the built in help command for discord.py

Based on the DefaultHelpCommand that discord.py uses, but revised for embeds and cogs on individual pages that can be "scrolled" through with reactions.

It's not clean, just something I've been meaning to do for a while and finally had an afternoon to look into it.

## Usage:

Example of how to use it:

```python
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp())
```

By default, the help will just pick a random color on every invoke. You can change this using the `color` argument:

```python
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="!", help_command=PrettyHelp(color=discord.Color.dark_gold()))
```

The basic `help` command will break commands up by cogs. Each cog will be a different page. Those pages can be navigated with
the arrow embeds. The message is unresponsive after 30s of no activity, it'll remove the reactions to let you know.

![example](https://raw.githubusercontent.com/stroupbslayen/discord-pretty-help/master/images/example.gif)

## Notes:
* `manage-messages` permission is recommended so reactions can be removed automatically

