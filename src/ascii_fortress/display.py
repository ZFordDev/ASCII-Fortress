"""Terminal space requirements shared by selection and gameplay."""

from blessed import Terminal


def required_size(rows: list[str]) -> tuple[int, int]:
    """Reserve room for the arena, compact HUD, and a spare column."""
    return max(40, max(map(len, rows), default=0)) + 1, len(rows) + 10


def fits(terminal: Terminal, width: int, height: int) -> bool:
    """Use character cells, not screen pixels, to check available space."""
    return terminal.width >= width and terminal.height >= height


def wait_for_space(terminal: Terminal, width: int, height: int) -> bool:
    """Pause until the arena fits; return False if the player leaves."""
    while not fits(terminal, width, height):
        # Clip the message too: even the resize screen must not scroll.
        lines = ("Paused: terminal too small.", f"Need {width} columns x {height} rows.",
                 "Resize to resume. Q: main menu.")
        print(terminal.home + terminal.clear, end="")
        for y, line in enumerate(lines[:max(0, terminal.height - 1)]):
            print(terminal.move_yx(y, 0) + line[:max(0, terminal.width - 1)], end="")
        print(end="", flush=True)
        if terminal.inkey(timeout=0.1).lower() == "q":
            return False
    return True
