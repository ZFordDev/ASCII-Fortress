# Maps

Each `.txt` file is one handcrafted map. Small loads `courtyard.txt` (21 x 11);
Medium loads `barracks.txt` (41 x 19). The launcher uses the selected map
for a movement prototype, placing the player at the start and replacing spawn
markers with ground. WASD moves one tile per received keypress and changes
facing, including when a wall blocks the step. Space fires a travelling `*`
bullet that disappears when it reaches a wall or the map boundary.

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

The barracks has four corner entrances, four solid bunk blocks, and a central
dividing wall with three passages. Every walkable tile connects to the player
start. The bunk blocks are excellent cover; actual beds are outside the budget.
