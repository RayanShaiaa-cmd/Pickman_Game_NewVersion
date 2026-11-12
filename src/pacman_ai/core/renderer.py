"""Rendering utilities for the Pac‑Man AI game.

All drawing is performed on the globally‑initialised pygame ``screen``. The
function ``render_game`` receives a ``GameState`` instance and paints the maze,
pellets, player and ghosts. Keeping rendering separate from the game‑logic
module makes the core loop testable without a graphical environment.
"""

"""Rendering utilities for the Pac‑Man AI game.

All drawing is performed on the globally‑initialised pygame ``screen``. The
function ``render_game`` receives a ``GameState``‑like object (any object that
exposes the attributes used below) and paints the maze, pellets, player and
ghosts. Keeping rendering separate from the game‑logic module avoids circular
imports and makes the core logic testable without a display.
"""

import pygame
from typing import Any

from ..config import settings

# The screen is created once at import time – this mirrors the original script
# but isolates the side‑effect from the rest of the code.
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Pac‑Man Multi Map (AI Predictive Avoidance - V3)")
font = pygame.font.SysFont('Arial', 28, bold=True)
small_font = pygame.font.SysFont('Arial', 20)


def render_game(state: Any) -> None:
    """Draw the current game state onto the global ``screen``.

    ``state`` must provide the attributes accessed below: ``maze``, ``pellets``,
    ``player.position``, ``player.is_ai``, ``score`` and an iterable ``ghosts``
    where each ghost has ``position`` and ``color``.
    """
    screen.fill(settings.BLACK)
    rows, cols = len(state.maze), len(state.maze[0])
    # Draw walls
    for r in range(rows):
        for c in range(cols):
            if state.maze[r][c] == 1:
                pygame.draw.rect(
                    screen,
                    settings.BLUE,
                    (c * settings.TILE, r * settings.TILE, settings.TILE, settings.TILE),
                )
    # Draw pellets
    for r, c in state.pellets:
        pygame.draw.circle(
            screen,
            settings.WHITE,
            (c * settings.TILE + settings.TILE // 2, r * settings.TILE + settings.TILE // 2),
            3,
        )
    # Draw player
    pr, pc = state.player.position
    pygame.draw.circle(
        screen,
        settings.YELLOW,
        (pc * settings.TILE + settings.TILE // 2, pr * settings.TILE + settings.TILE // 2),
        settings.TILE // 2 - 2,
    )
    # Draw ghosts
    for ghost in state.ghosts:
        gr, gc = ghost.position
        pygame.draw.circle(
            screen,
            ghost.color,
            (gc * settings.TILE + settings.TILE // 2, gr * settings.TILE + settings.TILE // 2),
            settings.TILE // 2 - 2,
        )
    # HUD – score and mode text
    screen.blit(font.render(f"Score: {state.score}", True, settings.WHITE), (10, 10))
    mode_text = "Auto (A* Safe)" if getattr(state.player, "is_ai", False) else "Manual"
    screen.blit(small_font.render(f"Mode: {mode_text}", True, settings.GRAY), (settings.WIDTH - 200, 10))
    screen.blit(small_font.render("G1 (Red): A* Direct", True, settings.RED), (settings.WIDTH - 200, 30))
    screen.blit(small_font.render("G2 (Pink): A* Ambush", True, settings.PINK), (settings.WIDTH - 200, 50))
    screen.blit(small_font.render("G3 (Green): BFS Simple", True, settings.GREEN), (settings.WIDTH - 200, 70))

    pygame.display.flip()
