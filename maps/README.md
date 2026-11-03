# Maps

| Size | File | Dimensions |
|---|---|---|
| Small | `courtyard.txt` | 21 x 11 |
| Medium | `barracks.txt` | 41 x 19 |
| Large | `stronghold.txt` | 61 x 27 |

Each file is a plain ASCII grid with equal-length rows and a solid outer wall.
Keep all walkable tiles connected. Explanations belong here, outside the grid.

| Symbol | Meaning |
|---|---|
| `#` | Wall |
| `.` | Ground |
| `^` | Exactly one player start, facing north |
| `X` | Zombie spawn, at least one per map |

Start and spawn tiles become ground when loaded. Spawn markers stay hidden.
Courtyard has inner walls, Barracks has bunk blocks, and Stronghold has long
sections linked by passages. Same terrible tenants, different floor plans.
