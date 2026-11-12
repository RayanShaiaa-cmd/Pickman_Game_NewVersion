"""Ghost AI strategies.

Each strategy implements ``next_move`` which receives the ghost's current position,
player position, the maze layout and an ``extra`` dictionary (used by the
ambush strategy to store the player's last known location).
"""

from __future__ import annotations

from typing import Tuple, List, Dict, Any, Optional

from ..ai.pathfinding import bfs_path, astar_path
from .prediction import calculate_ambush_target

Position = Tuple[int, int]
Maze = List[List[int]]


class GhostStrategy:
    """Base class – subclasses must implement ``next_move``."""

    def next_move(
        self,
        pos: Position,
        player_pos: Position,
        maze: Maze,
        extra: Dict[str, Any],
    ) -> Optional[Position]:
        raise NotImplementedError


class BFSStrategy(GhostStrategy):
    def next_move(self, pos: Position, player_pos: Position, maze: Maze, extra: Dict[str, Any]) -> Optional[Position]:
        path = bfs_path(pos, player_pos, maze)
        if path and len(path) > 1:
            return path[1]
        return None


class AStarDirectStrategy(GhostStrategy):
    def next_move(self, pos: Position, player_pos: Position, maze: Maze, extra: Dict[str, Any]) -> Optional[Position]:
        path = astar_path(pos, player_pos, maze)
        if path and len(path) > 1:
            return path[1]
        return None


class AStarAmbushStrategy(GhostStrategy):
    def next_move(self, pos: Position, player_pos: Position, maze: Maze, extra: Dict[str, Any]) -> Optional[Position]:
        last_player = extra.get("player_last_pos", player_pos)
        target = calculate_ambush_target(player_pos, last_player, maze)
        path = astar_path(pos, target, maze)
        if path and len(path) > 1:
            return path[1]
        return None


class GhostStrategyFactory:
    """Factory that returns a concrete strategy instance based on a name string."""

    _mapping = {
        "BFS_SIMPLE": BFSStrategy,
        "A_STAR_DIRECT": AStarDirectStrategy,
        "A_STAR_AMBUSH": AStarAmbushStrategy,
    }

    @staticmethod
    def create(name: str) -> GhostStrategy:
        cls = GhostStrategyFactory._mapping.get(name)
        if cls is None:
            raise ValueError(f"Unknown ghost strategy: {name}")
        return cls()
