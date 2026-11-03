import sys
from collections import deque
from pathlib import Path
from time import monotonic

from blessed import Terminal

from ascii_fortress.menus import main_menu, map_size_menu
from ascii_fortress.settings import Settings


def is_walkable(rows: list[str], x: int, y: int) -> bool:
    """Check terrain bounds before allowing a player or bullet onto a tile."""
    return 0 <= y < len(rows) and 0 <= x < len(rows[y]) and rows[y][x] == "."


def next_step_toward(
    rows: list[str], start: tuple[int, int], goal: tuple[int, int]
) -> tuple[int, int]:
    """Find the first step on a shortest four-direction path, or stay put."""
    frontier = deque([start])
    previous = {start: start}
    # Breadth-first search explores nearby tiles before more distant ones.
    while frontier:
        x, y = frontier.popleft()
        if (x, y) == goal:
            step = goal
            while step != start and previous[step] != start:
                step = previous[step]
            return step
        for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            neighbor = (x + dx, y + dy)
            if neighbor not in previous and is_walkable(rows, *neighbor):
                previous[neighbor] = (x, y)
                frontier.append(neighbor)
    return start


def main() -> None:
    """Keep one terminal session open for the menu and fresh game runs."""
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
    settings = Settings()
    # Return here after each run rather than nesting menus or game sessions.
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        while main_menu(terminal, settings) == "play":
            if map_size_menu(terminal, settings) == "small":
                run_game(terminal, courtyard, settings)


def run_game(terminal: Terminal, courtyard: str, settings: Settings) -> None:
    """Play one fresh run using an already active terminal session."""
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
    spawn_points = [
        (x, y)
        for y, row in enumerate(rows)
        for x, tile in enumerate(row)
        if tile == "X"
    ]
    if not spawn_points:
        raise SystemExit("The courtyard must have at least one zombie spawn (X).")
    zombies: set[tuple[int, int]] = set()
    wave = 1
    wave_size = 2
    pending_spawns = wave_size
    spawn_cursor = 0
    kills = 0
    health = 3
    # Keep the terrain separate so walking away leaves ground behind.
    rows = [row.replace("X", ".").replace("^", ".") for row in rows]
    directions = {
        "w": (0, -1, "^"),
        "a": (-1, 0, "<"),
        "s": (0, 1, "v"),
        "d": (1, 0, ">"),
    }
    aim_x, aim_y = 0, -1
    # Each bullet stores (x, y, direction_x, direction_y).
    bullets: list[tuple[int, int, int, int]] = []
    bullet_step_seconds = 0.1
    next_bullet_step = monotonic() + bullet_step_seconds
    zombie_step_seconds = 0.5
    next_zombie_step = next_bullet_step - bullet_step_seconds + zombie_step_seconds

    print(terminal.home + terminal.clear, end="")
    print(settings.paint(terminal, "ASCII Fortress", "cyan"))
    print("No graphics. No mercy. Just zombies.")
    print()
    for row in rows:
        print(row)
    print()
    print("WASD: move and aim. Space: shoot.")
    print("Press Q to return to the main menu.", flush=True)
    print(f"Wave: {wave} | Health: {health} | Remaining: {pending_spawns} | Kills: {kills}", flush=True)

    # The map starts below the title, tagline, and blank line (row 3).
    for x, y in zombies:
        print(terminal.move_yx(y + 3, x) + settings.paint(terminal, "Z", "green"), end="")
    print(terminal.move_yx(player_y + 3, player_x) + settings.paint(terminal, facing, "cyan"), end="", flush=True)
    # Timed reads leave room for future game updates while nobody is typing.
    while True:
        # Input must not control bullet speed: idle shots keep travelling.
        timeout = 0.1 if health == 0 else max(0.0, next_bullet_step - monotonic())
        key = terminal.inkey(timeout=timeout).lower()
        if key == "q":
            break
        if health == 0:
            # Leave the final arena visible, but the run is over.
            continue

        old_player = (player_x, player_y)
        old_bullet_tiles = {(x, y) for x, y, _, _ in bullets}
        old_zombies = zombies.copy()
        now = monotonic()
        while health > 0 and now >= next_bullet_step:
            # Walls win every argument. Bullets disappear on contact.
            travelling_bullets = []
            for x, y, dx, dy in bullets:
                destination = (x + dx, y + dy)
                if not is_walkable(rows, *destination):
                    continue
                if destination in zombies:
                    zombies.remove(destination)
                    kills += 1
                else:
                    travelling_bullets.append((*destination, dx, dy))
            bullets = travelling_bullets
            # Advance pursuit on the simulation clock, even without input.
            if next_bullet_step >= next_zombie_step:
                pursuing_zombies = set()
                for position in zombies:
                    destination = next_step_toward(rows, position, (player_x, player_y))
                    # A blocked step into the player is a contact attack.
                    if destination == (player_x, player_y):
                        health = max(0, health - 1)
                        destination = position
                    # Preserve every zombie: sets must not merge two bodies.
                    if destination in zombies or destination in pursuing_zombies:
                        destination = position
                    hit = next(
                        (i for i, bullet in enumerate(bullets) if bullet[:2] == destination),
                        None,
                    )
                    if hit is not None:
                        bullets.pop(hit)
                        kills += 1
                    else:
                        pursuing_zombies.add(destination)
                zombies = pursuing_zombies
                # Admit one zombie per step, rotating through free entrances.
                bullet_tiles = {(x, y) for x, y, _, _ in bullets}
                if health > 0 and pending_spawns:
                    for offset in range(len(spawn_points)):
                        index = (spawn_cursor + offset) % len(spawn_points)
                        spawn = spawn_points[index]
                        if spawn not in zombies and spawn != (player_x, player_y) and spawn not in bullet_tiles:
                            zombies.add(spawn)
                            pending_spawns -= 1
                            spawn_cursor = (index + 1) % len(spawn_points)
                            break
                next_zombie_step += zombie_step_seconds
            next_bullet_step += bullet_step_seconds

        if health > 0 and key in directions:
            aim_x, aim_y, facing = directions[key]
            next_x, next_y = player_x + aim_x, player_y + aim_y
            if is_walkable(rows, next_x, next_y) and (next_x, next_y) not in zombies:
                player_x, player_y = next_x, next_y
        elif health > 0 and key == " ":
            # One shot per received Space, with no ammo limit or cooldown.
            shot_x, shot_y = player_x + aim_x, player_y + aim_y
            # An adjacent target is hit immediately instead of skipped over.
            if (shot_x, shot_y) in zombies:
                zombies.remove((shot_x, shot_y))
                kills += 1
            elif is_walkable(rows, shot_x, shot_y):
                bullets.append((shot_x, shot_y, aim_x, aim_y))

        # A wave includes queued arrivals. No declaring victory at the door.
        if health > 0 and not zombies and pending_spawns == 0:
            wave += 1
            wave_size *= 2
            pending_spawns = wave_size

        # Restore terrain first, then bullets, then the player on top.
        for x, y in old_bullet_tiles | old_zombies | {old_player}:
            print(terminal.move_yx(y + 3, x) + rows[y][x], end="")
        for x, y, _, _ in bullets:
            print(terminal.move_yx(y + 3, x) + settings.paint(terminal, "*", "yellow"), end="")
        for x, y in zombies:
            print(terminal.move_yx(y + 3, x) + settings.paint(terminal, "Z", "green"), end="")
        remaining = len(zombies) + pending_spawns
        status = f"Wave: {wave} | Health: {health} | Remaining: {remaining} | Kills: {kills}"
        if health == 0:
            status += " | Game over. Q: main menu."
        print(
            terminal.move_yx(len(rows) + 6, 0) + status + terminal.clear_eol,
            end="",
        )
        print(terminal.move_yx(player_y + 3, player_x) + settings.paint(terminal, facing, "cyan"), end="", flush=True)
