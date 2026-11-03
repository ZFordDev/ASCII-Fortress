"""Terminal menus, kept separate from the survival simulation."""

from blessed import Terminal

from ascii_fortress.settings import Settings
from ascii_fortress.display import fits, required_size
from ascii_fortress.difficulty import Difficulty, PRESETS


def show_page(terminal: Terminal, settings: Settings, title: str, lines: tuple[str, ...]) -> None:
    """Show a short information page, then return to the existing menu."""
    print(terminal.home + terminal.clear, end="")
    print(settings.paint(terminal, title, "cyan"))
    print()
    for line in lines:
        print(line)
    print()
    print("Enter, Escape, or Q: back to main menu.", flush=True)
    while True:
        key = terminal.inkey()
        if key.name in ("KEY_ENTER", "KEY_ESCAPE") or key in ("\r", "\n", "\x1b") or key.lower() == "q":
            return


def settings_menu(terminal: Terminal, settings: Settings) -> None:
    """Toggle session colour without forcing effects on the player."""
    while True:
        print(terminal.home + terminal.clear, end="")
        print(settings.paint(terminal, "Settings", "cyan"))
        print()
        state = "On" if settings.colour else "Off"
        print(settings.paint(terminal, f"> Colour: {state}", "cyan"))
        print("Enter or Space: toggle. Escape or Q: back.")
        print("Applies to this session. New launches start with colour Off.", flush=True)
        key = terminal.inkey()
        if key.name == "KEY_ESCAPE" or key == "\x1b" or key.lower() == "q":
            return
        if key.name == "KEY_ENTER" or key in ("\r", "\n", " "):
            settings.colour = not settings.colour


def map_size_menu(terminal: Terminal, settings: Settings, maps: dict[str, str]) -> str | None:
    """Choose an available size, or go back without starting a run."""
    sizes = ("small", "medium", "large")
    selected = 0
    while True:
        options = []
        for size in sizes:
            if size not in maps:
                options.append(f"{size.title()} (coming soon)")
                continue
            width, height = required_size(maps[size].splitlines())
            label = f"{size.title()} (needs {width} x {height} terminal)"
            if not fits(terminal, width, height):
                label += " - too small"
            options.append(label)
        print(terminal.home + terminal.clear, end="")
        print(settings.paint(terminal, "Choose map size", "cyan"))
        print("More arena tiles, not bigger characters.")
        print()
        for index, label in enumerate(options):
            marker = ">" if index == selected else " "
            text = f"{marker} {label}"
            print(settings.paint(terminal, text, "cyan") if index == selected else text)
        print()
        print("Up/Down or W/S: select. Enter: confirm. Escape or Q: back.", flush=True)
        key = terminal.inkey(timeout=0.1)
        if not key:
            continue
        if key.name == "KEY_ESCAPE" or key == "\x1b" or key.lower() == "q":
            return None
        if key.name == "KEY_UP" or key.lower() == "w":
            selected = (selected - 1) % len(options)
        elif key.name == "KEY_DOWN" or key.lower() == "s":
            selected = (selected + 1) % len(options)
        elif key.name == "KEY_ENTER" or key in ("\r", "\n"):
            size = sizes[selected]
            if size in maps and fits(terminal, *required_size(maps[size].splitlines())):
                return size
            # Keep unavailable sizes on this screen until their maps exist.


def difficulty_menu(terminal: Terminal, settings: Settings) -> Difficulty | None:
    """Choose run rules, or return to map-size selection."""
    selected = 0
    while True:
        print(terminal.home + terminal.clear, end="")
        print(settings.paint(terminal, "Choose difficulty", "cyan"))
        print()
        for index, preset in enumerate(PRESETS):
            marker = ">" if index == selected else " "
            text = f"{marker} {preset.name}"
            print(settings.paint(terminal, text, "cyan") if index == selected else text)
        print()
        print(PRESETS[selected].description)
        print("W/S or Up/Down: select. Enter: play.")
        print("Escape or Q: back to map size.", flush=True)
        key = terminal.inkey()
        if key.name == "KEY_ESCAPE" or key == "\x1b" or key.lower() == "q":
            return None
        if key.name == "KEY_UP" or key.lower() == "w":
            selected = (selected - 1) % len(PRESETS)
        elif key.name == "KEY_DOWN" or key.lower() == "s":
            selected = (selected + 1) % len(PRESETS)
        elif key.name == "KEY_ENTER" or key in ("\r", "\n"):
            return PRESETS[selected]


def game_over_menu(
    terminal: Terminal, settings: Settings, difficulty: Difficulty, wave: int, kills: int
) -> str:
    """Offer a fresh run with the same choices, the main menu, or a clean exit."""
    options = (("Play again", "replay"), ("Main menu", "menu"), ("Quit", "quit"))
    selected = 0
    while True:
        print(terminal.home + terminal.clear, end="")
        print(settings.paint(terminal, "Game over", "cyan"))
        print(f"Difficulty: {difficulty.name}")
        print(f"Wave reached: {wave} | Kills: {kills}")
        print("The zombies would like to thank you for lunch.")
        print()
        for index, (label, _) in enumerate(options):
            marker = ">" if index == selected else " "
            text = f"{marker} {label}"
            print(settings.paint(terminal, text, "cyan") if index == selected else text)
        print()
        print("W/S or Up/Down: select. Enter: confirm.")
        print("Escape: main menu. Q: quit.", flush=True)
        key = terminal.inkey()
        if key.lower() == "q":
            return "quit"
        if key.name == "KEY_ESCAPE" or key == "\x1b":
            return "menu"
        if key.name == "KEY_UP" or key.lower() == "w":
            selected = (selected - 1) % len(options)
        elif key.name == "KEY_DOWN" or key.lower() == "s":
            selected = (selected + 1) % len(options)
        elif key.name == "KEY_ENTER" or key in ("\r", "\n"):
            return options[selected][1]


def main_menu(terminal: Terminal, settings: Settings) -> str:
    """Wait for Play or Quit, with optional pages sharing session settings."""
    options = (
        "Play",
        "How to",
        "Settings",
        "Credits",
        "Quit",
    )
    selected = 0
    while True:
        print(terminal.home + terminal.clear, end="")
        print(settings.paint(terminal, "ASCII Fortress", "cyan"))
        print("No graphics. No mercy. Just zombies.")
        print()
        for index, label in enumerate(options):
            marker = ">" if index == selected else " "
            text = f"{marker} {label}"
            print(settings.paint(terminal, text, "cyan") if index == selected else text)
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
                show_page(terminal, settings, "How to survive (briefly)", (
                    "WASD: move and face that direction.",
                    "Space: shoot where you face. Ammo is unlimited.",
                    "Walls stop you, zombies, and bullets.",
                    "Z means zombie. Tougher modes need more hits.",
                    "You have 3 health. Zombie contact hurts. No healing.",
                    "Clear a wave. Next wave has twice the zombies.",
                    "Survive as many waves as you can.",
                    "Q during a run: return to the main menu.",
                    "",
                    "Ammo is unlimited. Your personal space is not.",
                ))
            elif selected == 2:
                settings_menu(terminal, settings)
            elif selected == 3:
                show_page(terminal, settings, "Credits", (
                    "ASCII Fortress", "Development: ZFordDev", "",
                    "Zombies: unpaid extras. Still demanding more brains.",
                ))
