__all__ = ["Navigation"]


class Navigation:
    """A class to aid in customizing the navigation menu for PrettyHelp.
    Accepts standard emojis in multiple ways:
        - Emoji:: "👍"
        - Unicode:: "\\U0001F44D"
        - Unicode Name:: "\\N{THUMBS UP SIGN}"

    Using a custom emoji:
        - Discord emoji id:: ":custom_emoji:8675309"

    Use `\` to get the discord representation:
        Example: '\\\:custom_emoji:' in discord

    Args:
        page_left (str, optional): The emoji to use for going left. Defaults to "◀".
        page_right (str, optional): The emoji to use for going right. Defaults to "▶".
        remove (str, optional): The emoji to use for removing the help message. Defaults to "❌".
    """

    def __init__(self, page_left="◀", page_right="▶", remove="❌") -> None:
        self.page_left = page_left
        self.page_right = page_right
        self.remove = remove

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

    def __iter__(self):
        return self._dict.__iter__()

    def __repr__(self) -> str:
        return f"<Navigation left:{self.page_left} right:{self.page_right} remove:{self.remove}>"
