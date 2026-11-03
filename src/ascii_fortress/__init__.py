import sys
from pathlib import Path

from blessed import Terminal


def main() -> None:
    """Show the courtyard preview and wait for the player to quit."""
    # Keyboard input needs a real terminal, rather than a pipe or output file.
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Run ASCII Fortress in an interactive terminal.")
        return

    # Resolve from the source file so launching from another folder still works.
    map_path = Path(__file__).resolve().parents[2] / "maps" / "courtyard.txt"
    try:
        courtyard = map_path.read_text(encoding="ascii")
    except (OSError, UnicodeError) as error:
        # Load before entering fullscreen so errors stay visible in the shell.
        raise SystemExit(f"Could not load courtyard map: {error}") from error

    terminal = Terminal()
    # Context managers restore the screen, cursor, and input mode on exit.
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.clear, end="")
        print("ASCII Fortress")
        print("No graphics. No mercy. Just zombies.")
        print()
        # Spawn markers are map instructions, not visible arena tiles.
        print(courtyard.replace("X", ".").rstrip("\r\n"))
        print()
        print("Courtyard preview. Movement and shooting are coming soon.")
        print("Press Q to quit.", flush=True)

        # Timed reads leave room for future game updates while nobody is typing.
        while True:
            key = terminal.inkey(timeout=0.1)
            if key.lower() == "q":
                break
