"""Safe navigation for the AI-controlled player.

The function ``find_safe_path_astar`` mirrors the original project's AI that
collects the nearest pellet while avoiding predicted ghost paths. It uses the
generic ``astar_custom_path`` with a cost function that penalises cells that are
part of any predicted ghost trajectory.
"""

from __future__ import annotations

from typing import Set, List, Tuple, Dict

from config import settings
from .pathfinding import astar_custom_path, neighbors
from .prediction import predict_ghost_paths

Position = Tuple[int, int]
Maze = List[List[int]]


def find_safe_path_astar(
    src: Position,
    pellets: Set[Position],
    maze: Maze,
    ghosts: List[object],
    player_pos: Position,
) -> List[Position] | None:
    """Return a safe path from ``src`` to the nearest pellet.

    The algorithm:

    1. Predict ghost trajectories for ``settings.PREDICTION_STEPS`` steps.
    2. Build a cost function that assigns a huge penalty (``settings.PATH_PENALTY``)
       to any cell that appears in the predicted paths, effectively turning it
       into a wall for the A* search.
    3. Perform a BFS to locate the nearest pellet (ignoring threats).
    4. Run weighted A* with the anti‑ghost cost. If no safe path is found, fall
       back to a random safe neighbour, and as a last resort a random move.
    """

    # 1. Predict ghost future cells
    predicted = predict_ghost_paths(player_pos, maze, ghosts)
    threat_cells: Set[Position] = set()
    for cells in predicted.values():
        threat_cells.update(cells)

    # 2. Cost function
    def anti_cost(node: Position) -> int:
        if node in threat_cells:
            return settings.PATH_PENALTY
        # Additional distance‑based penalty to stay away from nearby ghosts
        for g in ghosts:
            dist = abs(node[0] - g.position[0]) + abs(node[1] - g.position[1])
            if dist < 3:
                # The closer the ghost, the higher the extra cost
                return settings.PATH_PENALTY // (dist + 1)
        return 1

    # 3. Locate the nearest pellet (simple BFS)
    from collections import deque

    visited: Set[Position] = {src}
    q = deque([src])
    nearest: Position | None = None
    while q:
        cur = q.popleft()
        if cur in pellets:
            nearest = cur
            break
        for nb in neighbors(cur, maze):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    if nearest is None:
        return None

    # 4. Weighted A* to the chosen pellet
    path = astar_custom_path(src, nearest, maze, anti_cost)
    if path and len(path) > 1:
        return path
    # Fallback: choose any safe neighbour
    safe_moves = [n for n in neighbors(src, maze) if anti_cost(n) < settings.PATH_PENALTY]
    if safe_moves:
        return [src, safe_moves[0]]
    # Last resort: any move
    all_moves = list(neighbors(src, maze))
    if all_moves:
        return [src, all_moves[0]]
    return None
