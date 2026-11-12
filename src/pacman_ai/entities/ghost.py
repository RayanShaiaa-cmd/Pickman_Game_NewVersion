"""Ghost entity and strategy handling.

Each ghost stores its position, colour, movement speed, cooldown counter and a
reference to a concrete strategy object that knows how to compute the next
position given the current maze and player location.
"""

from __future__ import annotations

from typing import Tuple, List, Dict, Any

from ..config import settings
from ..ai.strategies import GhostStrategyFactory


class Ghost:
    """Represent a ghost.

    Parameters
    ----------
    start_pos: Tuple[int, int]
        Initial grid coordinates.
    color: Tuple[int, int, int]
        RGB colour used for rendering.
    strategy_name: str
        Identifier passed to :class:`GhostStrategyFactory` (e.g. ``"BFS_SIMPLE"``).
    speed: int, optional
        Number of ticks between moves (default 1 – move every tick).
    extra: dict, optional
        Additional per‑ghost state (e.g. ``player_last_pos`` for the ambusher).
    """

    def __init__(
        self,
        start_pos: Tuple[int, int],
        color: Tuple[int, int, int],
        strategy_name: str,
        speed: int = 1,
        extra: Dict[str, Any] | None = None,
    ) -> None:
        self.position: Tuple[int, int] = start_pos
        self.color = color
        self.strategy_name = strategy_name
        self.speed = speed
        self.cooldown: int = 0
        self.moves: int = 0
        self.extra: Dict[str, Any] = extra.copy() if extra else {}
        # Strategy object that knows how to compute the next move
        self.strategy = GhostStrategyFactory.create(strategy_name)

    def update(self, maze: List[List[int]], player_pos: Tuple[int, int]) -> None:
        """Update the ghost for a single tick.

        The ghost moves only when its cooldown reaches ``0``. After moving the
        cooldown is reset to ``speed - 1``.
        """
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        # Compute next position via the strategy
        next_pos = self.strategy.next_move(self.position, player_pos, maze, self.extra)
        if next_pos is not None:
            self.position = next_pos
            self.moves += 1
        self.cooldown = self.speed - 1

    # Helper for UI end‑screen (expects a dict‑like representation)
    def as_dict(self) -> Dict[str, Any]:
        return {
            "pos": list(self.position),
            "color": self.color,
            "strategy": self.strategy_name,
            "speed": self.speed,
            "cooldown": self.cooldown,
            "moves": self.moves,
            "name": self.extra.get("name", self.strategy_name),
            "player_last_pos": self.extra.get("player_last_pos"),
        }
