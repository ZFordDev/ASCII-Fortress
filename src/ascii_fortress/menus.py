"""Terminal menus, kept separate from the survival simulation."""

from blessed import Terminal


def show_page(terminal: Terminal, title: str, lines: tuple[str, ...]) -> None:
    """Show a short information page, then return to the existing menu."""
    print(terminal.home + terminal.clear, end="")
    print(title)
    print()
    for line in lines:
        print(line)
    print()
    print("Enter, Escape, or Q: back to main menu.", flush=True)
    while True:
        key = terminal.inkey()
        if key.name in ("KEY_ENTER", "KEY_ESCAPE") or key in ("\r", "\n", "\x1b") or key.lower() == "q":
            return


def main_menu(terminal: Terminal) -> str:
    """Wait for Play or Quit; unfinished pages cannot be opened yet."""
    options = (
        "Play",
        "How to",
        "Settings (coming soon)",
        "Credits",
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
            if selected == 1:
                show_page(terminal, "How to survive (briefly)", (
                    "WASD: move and face that direction.",
                    "Space: shoot where you face. Ammo is unlimited.",
                    "Walls stop you, zombies, and bullets.",
                    "Z means zombie. One bullet sorts it out.",
                    "You have 3 health. Zombie contact hurts. No healing.",
                    "Clear a wave. Next wave has twice the zombies.",
                    "Survive as many waves as you can.",
                    "Q during a run: return to the main menu.",
                    "",
                    "Ammo is unlimited. Your personal space is not.",
                ))
            elif selected == 3:
                show_page(terminal, "Credits", (
                    "ASCII Fortress", "Development: ZFordDev", "",
                    "Zombies: unpaid extras. Still demanding more brains.",
                ))
            # Settings stays labelled coming soon until its controls exist.
