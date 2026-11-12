"""Random maze generator.

The algorithm is a simple depth‑first maze carving implementation identical to
the original ``generate_random_maze`` function.
"""

import random
from typing import List

from ..config import settings


def generate_random_maze(rows: int = settings.ROWS, cols: int = settings.COLS) -> List[List[int]]:
    """Return a randomly carved maze.

    The returned structure matches the format of the hard‑coded maps: ``1`` for
    walls, ``0`` for free cells. The outer border is always walls.
    """
    maze = [[1] * cols for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = 0
    while stack:
        current_r, current_c = stack[-1]
        unvisited = []
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = current_r + dr, current_c + dc
            if 0 < nr < rows - 1 and 0 < nc < cols - 1 and maze[nr][nc] == 1:
                unvisited.append((nr, nc))
        if unvisited:
            next_r, next_c = random.choice(unvisited)
            maze[(current_r + next_r) // 2][(current_c + next_c) // 2] = 0
            maze[next_r][next_c] = 0
            stack.append((next_r, next_c))
        else:
            stack.pop()
    return maze
