"""Initial difficulty values, kept together for small balance changes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Difficulty:
    """Run rules; presentation settings live separately."""

    name: str
    movement_seconds: float
    spawn_seconds: float
    zombie_health: int
    description: str


PRESETS = (
    Difficulty("Easy", 0.50, 0.50, 1, "Original pace. One hit per zombie."),
    Difficulty("Normal", 0.40, 0.40, 1, "Faster feet. Still one hit."),
    Difficulty("Hard", 0.30, 0.25, 2, "Fast arrivals. Two hits per zombie."),
    Difficulty("Insane", 0.15, 0.15, 3, "Very fast. Three hits. Bring regrets."),
)
