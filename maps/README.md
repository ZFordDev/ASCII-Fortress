# Maps

Each `.txt` file is one handcrafted map. `courtyard.txt` is the first test map;
the game does not load it yet.

Keep map files as plain ASCII grids with equal-length rows and a solid outer
wall. Put explanations here rather than inside the grid, where every character
is a tile.

| Symbol | Meaning |
|---|---|
| `#` | Solid wall |
| `.` | Walkable ground |
| `^` | Player starting position, facing north (exactly one per map) |
| `X` | Zombie spawn point (at least one per map) |

Player and zombie spawn tiles are walkable ground once their markers are read.
Spawn markers are map data and will not be shown during gameplay.

The courtyard has four zombie entrances and gaps in its inner walls to keep
the walkable area connected. Apparently, fortress security took the day off.
