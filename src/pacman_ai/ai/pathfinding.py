"""AI subpackage – path‑finding utilities used by both player and ghosts.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Callable, List, Tuple, Set

Position = Tuple[int, int]
Maze = List[List[int]]


def neighbors(cell: Position, maze: Maze) -> Set[Position]:
    """Yield walkable orthogonal neighbours of ``cell``.

    Parameters
    ----------
    cell: (row, col)
    maze: 2‑D grid where ``0`` is free and ``1`` is a wall.
    """
    r, c = cell
    rows, cols = len(maze), len(maze[0])
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            yield (nr, nc)


def bfs_path(src: Position, dst: Position, maze: Maze) -> List[Position] | None:
    """Return the shortest unweighted path from ``src`` to ``dst`` using BFS.

    Returns ``None`` if ``dst`` is unreachable.
    """
    if src == dst:
        return [src]
    q = deque([src])
    prev: dict[Position, Position | None] = {src: None}
    visited: Set[Position] = {src}
    while q:
        cur = q.popleft()
        for nb in neighbors(cur, maze):
            if nb not in visited:
                visited.add(nb)
                prev[nb] = cur
                if nb == dst:
                    # Reconstruct path
                    path = [dst]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])  # type: ignore[arg-type]
                    return list(reversed(path))
                q.append(nb)
    return None


def h_manhattan(a: Position, b: Position) -> int:
    """Manhattan distance heuristic for grid movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_custom_path(
    src: Position,
    dst: Position,
    maze: Maze,
    cost_func: Callable[[Position], int],
    heuristic_func: Callable[[Position, Position], int] = h_manhattan,
) -> List[Position] | None:
    """Weighted A* search.

    ``cost_func`` returns a multiplier applied to the uniform step cost (1).  A
    large multiplier can effectively turn a cell into a wall.
    """
    open_set: List[Tuple[int, int, Position]] = [
        (heuristic_func(src, dst), 0, src)
    ]  # (f, g, node)
    came: dict[Position, Position | None] = {src: None}
    g_score: dict[Position, int] = {src: 0}
    closed: Set[Position] = set()

    while open_set:
        f, cost, cur = heapq.heappop(open_set)
        if cur == dst:
            # Reconstruct path
            path = [cur]
            while came[path[-1]] is not None:
                path.append(came[path[-1]])  # type: ignore[arg-type]
            return list(reversed(path))

        if cur in closed:
            continue
        closed.add(cur)

        cur_multiplier = cost_func(cur)
        if cur_multiplier > 1000:
            # Treat extremely costly nodes as impassable
            continue

        for nb in neighbors(cur, maze):
            nb_multiplier = cost_func(nb)
            tentative_g = cost + nb_multiplier * 1
            if nb not in g_score or tentative_g < g_score[nb]:
                g_score[nb] = tentative_g
                f_nb = tentative_g + heuristic_func(nb, dst)
                heapq.heappush(open_set, (f_nb, tentative_g, nb))
                came[nb] = cur
    return None


def astar_path(src: Position, dst: Position, maze: Maze) -> List[Position] | None:
    """Convenience wrapper for unweighted A* (all costs = 1)."""
    return astar_custom_path(src, dst, maze, lambda _: 1)
