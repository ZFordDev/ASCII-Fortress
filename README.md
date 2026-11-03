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

Development has just started. The launcher currently shows a welcome message, planned controls, and the survival goal, gameplay is coming later. The zombies are still getting dressed.

With [uv](https://docs.astral.sh/uv/) installed, run the following from the project directory (the folder containing `pyproject.toml`):

```sh
uv run ascii-fortress
```

The project requires Python 3.12 or newer. uv manages the project environment and installs the package when you run it.

## More Info

Want the nerdy details? Check out the [GitHub Wiki](../../wiki).

## License

Free and open source under the [Apache License 2.0](LICENSE).
