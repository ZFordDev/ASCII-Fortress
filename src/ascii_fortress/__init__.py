import sys
from pathlib import Path

from blessed import Terminal


def main() -> None:
    """Explore the courtyard with WASD, or press Q to quit."""
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

    rows = courtyard.splitlines()
    starts = [
        (x, y)
        for y, row in enumerate(rows)
        for x, tile in enumerate(row)
        if tile == "^"
    ]
    if len(starts) != 1:
        raise SystemExit("The courtyard must have exactly one player start (^).")

    player_x, player_y = starts[0]
    facing = "^"
    # Keep the terrain separate so walking away leaves ground behind.
    rows = [row.replace("X", ".").replace("^", ".") for row in rows]
    directions = {
        "w": (0, -1, "^"),
        "a": (-1, 0, "<"),
        "s": (0, 1, "v"),
        "d": (1, 0, ">"),
    }

    terminal = Terminal()
    # Context managers restore the screen, cursor, and input mode on exit.
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        print(terminal.home + terminal.clear, end="")
        print("ASCII Fortress")
        print("No graphics. No mercy. Just zombies.")
        print()
        for row in rows:
            print(row)
        print()
        print("WASD: move and aim. Shooting is coming soon.")
        print("Press Q to quit.", flush=True)

        # The map starts below the title, tagline, and blank line (row 3).
        print(terminal.move_yx(player_y + 3, player_x) + facing, end="", flush=True)
        # Timed reads leave room for future game updates while nobody is typing.
        while True:
            key = terminal.inkey(timeout=0.1).lower()
            if key == "q":
                break
            if key not in directions:
                continue

            dx, dy, facing = directions[key]
            next_x, next_y = player_x + dx, player_y + dy
            # Check bounds as well as walls. No escaping through Python indexes.
            if (
                0 <= next_y < len(rows)
                and 0 <= next_x < len(rows[next_y])
                and rows[next_y][next_x] == "."
            ):
                print(terminal.move_yx(player_y + 3, player_x) + ".", end="")
                player_x, player_y = next_x, next_y

            # Facing changes even when a wall blocks the step.
            print(terminal.move_yx(player_y + 3, player_x) + facing, end="", flush=True)
