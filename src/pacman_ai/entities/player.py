"""Player entity.

The player can be controlled manually via keyboard or operate autonomously
(using the safe‑navigation AI). The class stores the current grid position
as a ``(row, col)`` tuple.
"""

from __future__ import annotations

from typing import Tuple, List

import pygame

from ..config import settings


class Player:
    """Represent the Pac‑Man player.

    Parameters
    ----------
    start_pos: Tuple[int, int]
        Initial ``(row, col)`` location.
    is_ai: bool
        ``True`` enables autonomous movement; ``False`` enables manual control.
    """

    def __init__(self, start_pos: Tuple[int, int], is_ai: bool) -> None:
        self.position: Tuple[int, int] = start_pos
        self.is_ai: bool = is_ai

    def handle_key(self, key: int, maze: List[List[int]]) -> None:
        """Update ``self.position`` based on a pressed arrow key.

        The method is a thin wrapper around the original script's manual input
        handling. It ignores keys that would move into a wall.
        """
        r, c = self.position
        if key == pygame.K_UP:
            nr, nc = r - 1, c
        elif key == pygame.K_DOWN:
            nr, nc = r + 1, c
        elif key == pygame.K_LEFT:
            nr, nc = r, c - 1
        elif key == pygame.K_RIGHT:
            nr, nc = r, c + 1
        else:
            return
        rows, cols = len(maze), len(maze[0])
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            self.position = (nr, nc)
