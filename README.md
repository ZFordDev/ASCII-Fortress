# ASCII Fortress

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

**No graphics. No mercy. Just zombies.**

ASCII Fortress is a tiny terminal-based zombie survival game written in Python.

Grab your imaginary gun, find a chokepoint, and survive increasingly ridiculous waves of zombies. They're not particularly smart, but there's a lot of them.

## 🎮 How to Play

| Key | Action |
|---|---|
| `W A S D` | Move and aim |
| `Space` | Shoot. A lot. |

- Unlimited ammo. Reloading is overrated.
- Zombies double every wave. Good luck with that.
- 4–5 handcrafted maps with walls and chokepoints.
- No healing. No second chances.
- One goal: survive longer than last time.

## Getting Started

Development has just started. Explore the fullscreen courtyard with `WASD`, fire with `Space`, and press `Q` to quit. Walls block movement, and your character turns to face the direction you press. Bullets travel in that direction and stop at walls.

One stationary `Z` target appears at the first map spawn point (top-left in the
courtyard). It blocks movement and disappears after one bullet hit, increasing
the displayed kill count. Restart the command for another target. Zombie
pursuit, player damage, and waves are coming later.

Movement currently advances one tile per received keypress; holding a key uses
your terminal's keyboard repeat behaviour.
Each received Space fires one bullet, with unlimited ammo and no firing cooldown.
Bullets move ten tiles per second independently of keyboard input. Holding keys
and moving while shooting still need testing on Windows and Linux terminals.

With [uv](https://docs.astral.sh/uv/) installed, run the following from the project directory (the folder containing `pyproject.toml`):

```sh
uv run ascii-fortress
```

The project requires Python 3.12 or newer. uv manages the project environment and installs the package when you run it.

Run in an interactive terminal, such as Windows Terminal or a Linux terminal.

The preview currently loads `maps/courtyard.txt` from the source checkout.
Keep that folder alongside `src`; standalone package distribution is a later step.

## More Info

Want the nerdy details? Check out the [GitHub Wiki](../../wiki).

## License

Free and open source under the [Apache License 2.0](LICENSE).
