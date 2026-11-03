import sys

from blessed import Terminal


def main() -> None:
    """Show a fullscreen welcome and wait for the player to quit."""
    # Keyboard input needs a real terminal, rather than a pipe or output file.
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Run ASCII Fortress in an interactive terminal.")
        return

    terminal = Terminal()
    # Context managers restore the screen, cursor, and input mode on exit.
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.clear, end="")
        print("ASCII Fortress")
        print("No graphics. No mercy. Just zombies.")
        print()
        print("Planned controls: WASD to move and aim, Space to shoot.")
        print("Goal: survive as many waves as you can.")
        print("Gameplay is coming soon. The zombies are still getting dressed.")
        print()
        print("Press Q to quit.", flush=True)

        # Timed reads leave room for future game updates while nobody is typing.
        while True:
            key = terminal.inkey(timeout=0.1)
            if key.lower() == "q":
                break
