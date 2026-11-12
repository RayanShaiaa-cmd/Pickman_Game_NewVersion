"""Prediction utilities for ghost movement and ambush targeting.

The functions are extracted from the original monolithic script to keep the AI
logic self‑contained and testable.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from config import settings
from ..ai.pathfinding import bfs_path, astar_path

Position = Tuple[int, int]
Maze = List[List[int]]


def calculate_ambush_target(player_pos: Position, last_player_pos: Position, maze: Maze) -> Position:
    """Return a cell a fixed distance ahead of the player in the direction of motion.

    Mirrors the original implementation: it looks four tiles ahead (``settings.AMBUSH_DISTANCE``)
    and falls back to the player position if the target is out of bounds or a wall.
    """
    rows, cols = len(maze), len(maze[0])
    pr, pc = player_pos
    plr, plc = last_player_pos
    dr, dc = pr - plr, pc - plc
    target_r = pr + dr * settings.AMBUSH_DISTANCE
    target_c = pc + dc * settings.AMBUSH_DISTANCE
    if 0 <= target_r < rows and 0 <= target_c < cols and maze[target_r][target_c] == 0:
        return (target_r, target_c)
    return player_pos


def predict_ghost_paths(player_pos: Position, maze: Maze, ghosts: List[object]) -> Dict[str, Set[Position]]:
    """Predict future cells for each ghost.

    Returns a mapping ``{ghost_name: set_of_future_cells}``. The ``ghosts`` list
    should contain objects that expose ``position``, ``strategy_name`` and, for
    the ambush strategy, an ``extra`` dict with ``player_last_pos``.
    """
    steps = settings.PREDICTION_STEPS
    result: Dict[str, Set[Position]] = {}
    for g in ghosts:
        pos = g.position
        strat = g.strategy_name
        path: List[Position] | None = None
        if strat == "BFS_SIMPLE":
            path = bfs_path(pos, player_pos, maze)
        elif strat == "A_STAR_DIRECT":
            path = astar_path(pos, player_pos, maze)
        elif strat == "A_STAR_AMBUSH":
            target = calculate_ambush_target(player_pos, g.extra.get("player_last_pos", player_pos), maze)
            path = astar_path(pos, target, maze)
        if path:
            result[g.strategy_name] = set(path[1 : steps + 1])
    return result
