# Maps

Each `.txt` file is one handcrafted map. The launcher loads `courtyard.txt`
for a static preview, showing the player start and replacing spawn markers
with ground. Movement and shooting are not implemented yet.

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
