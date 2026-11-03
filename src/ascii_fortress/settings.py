"""Optional presentation preferences for the current session."""

from dataclasses import dataclass

from blessed import Terminal


@dataclass
class Settings:
    """Start plain; changing these preferences never changes game rules."""

    colour: bool = False

    def paint(self, terminal: Terminal, text: str, colour: str) -> str:
        """Return plain text unless the player opts into colour."""
        if not self.colour:
            return text
        # Blessed's callable styles reset formatting after each piece of text.
        return getattr(terminal, colour)(text)
