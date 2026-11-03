"""Terminal menus, kept separate from the survival simulation."""

from blessed import Terminal


def main_menu(terminal: Terminal) -> str:
    """Wait for Play or Quit; unfinished pages cannot be opened yet."""
    options = (
        "Play",
        "How to (coming soon)",
        "Settings (coming soon)",
        "Credits (coming soon)",
        "Quit",
    )
    selected = 0
    while True:
        print(terminal.home + terminal.clear, end="")
        print("ASCII Fortress")
        print("No graphics. No mercy. Just zombies.")
        print()
        for index, label in enumerate(options):
            marker = ">" if index == selected else " "
            print(f"{marker} {label}")
        print()
        print("Up/Down or W/S: select. Enter: confirm. Q: quit.", flush=True)

        # Keep the Keystroke object: special keys carry names as well as text.
        key = terminal.inkey()
        if key.lower() == "q":
            return "quit"
        if key.name == "KEY_UP" or key.lower() == "w":
            selected = (selected - 1) % len(options)
        elif key.name == "KEY_DOWN" or key.lower() == "s":
            selected = (selected + 1) % len(options)
        elif key.name == "KEY_ENTER" or key in ("\r", "\n"):
            if selected == 0:
                return "play"
            if selected == len(options) - 1:
                return "quit"
            # Coming-soon entries stay on this screen. No mystery doors yet.
