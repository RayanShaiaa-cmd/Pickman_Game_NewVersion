"""Game state and manager for Pac‑Man AI.

The `GameManager` drives the main simulation loop. It holds a reference to the
current `GameState` (maze layout, pellet set, player/ghost objects, score, etc.)
and updates everything each tick. Rendering is delegated to
`pacman_ai.core.renderer` so that the manager stays logic‑only and can be unit
tested without a display.
"""

from __future__ import annotations

import random
from typing import List, Set, Tuple

import pygame

from ..config import settings
from ..entities.player import Player
from ..entities.ghost import Ghost, GhostStrategyFactory
from .renderer import render_game
from .ui import show_end_screen

# Type aliases for clarity
Position = Tuple[int, int]
Maze = List[List[int]]


class GameState:
    """Container for the mutable state of a running game.

    Attributes
    ----------
    maze: Maze
        2‑D grid where ``1`` denotes a wall and ``0`` a free cell.
    pellets: Set[Position]
        Set of all remaining pellet coordinates.
    player: Player
    ghosts: List[Ghost]
    score: int
    win: bool
    over: bool
    """

    def __init__(self, maze: Maze, difficulty: int, mode_auto: bool) -> None:
        self.maze = maze
        rows, cols = len(maze), len(maze[0])
        # Initialise pellets – every free cell is a pellet except the start cell
        self.pellets: Set[Position] = {
            (r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0
        }
        start: Position = (1, 1)
        if start in self.pellets:
            self.pellets.remove(start)

        self.player = Player(start, mode_auto)
        # Ghost initial positions are hard‑coded to match the original script
        self.ghosts = [
            Ghost((1, 26), settings.RED, "A_STAR_DIRECT"),
            Ghost((1, 27), settings.PINK, "A_STAR_AMBUSH", extra={"player_last_pos": start}),
            Ghost((1, 28), settings.GREEN, "BFS_SIMPLE"),
        ]
        self.score = 0
        self.win = False
        self.over = False
        self.difficulty = difficulty  # currently unused but kept for API stability

    @property
    def total_pellets(self) -> int:
        """Number of pellets that existed at the start of the level."""
        rows, cols = len(self.maze), len(self.maze[0])
        return sum(1 for r in range(rows) for c in range(cols) if self.maze[r][c] == 0)


class GameManager:
    """Runs the main game loop.

    The manager separates *logic* from *rendering* – the latter lives in
    ``pacman_ai.core.renderer``. This allows the loop to be exercised by unit
    tests in head‑less environments.
    """

    def __init__(self, maze: Maze, difficulty: int, mode_auto: bool) -> None:
        self.state = GameState(maze, difficulty, mode_auto)
        self.clock = pygame.time.Clock()
        self.auto_path: List[Position] | None = None
        # Pre‑compute total pellet count for win detection
        self._total_pellets = self.state.total_pellets + 1  # include start cell

    def run(self) -> None:
        """Execute the game until it ends (win or loss)."""
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                # Manual player input – only processed when not in AI mode
                if event.type == pygame.KEYDOWN and not self.state.player.is_ai:
                    self.state.player.handle_key(event.key, self.state.maze)

            # --- AI player movement ------------------------------------------------
            if self.state.player.is_ai and not (self.state.over or self.state.win):
                self._process_ai_move()

            # --- Pellet collection -------------------------------------------------
            player_pos = self.state.player.position
            if player_pos in self.state.pellets:
                self.state.pellets.remove(player_pos)
                self.state.score += 10
                if not self.state.pellets:
                    self.state.win = True

            # --- Ghost updates -----------------------------------------------------
            for ghost in self.state.ghosts:
                ghost.update(self.state.maze, player_pos)
                if ghost.position == player_pos:
                    self.state.over = True
                    break

            # --- Rendering --------------------------------------------------------
            render_game(self.state)

            # End‑game handling – break the loop so that the caller can show the
            # end screen and decide whether to restart.
            if self.state.over or self.state.win:
                break

    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------
    def _process_ai_move(self) -> None:
        """Calculate a safe path for the AI player and move one step.

        The heavy lifting is delegated to ``pacman_ai.ai.safe_navigation``.
        """
        from ..ai.safe_navigation import find_safe_path_astar

        if not self.auto_path or len(self.auto_path) <= 1:
            # Compute a new safe path towards the nearest pellet.
            path = find_safe_path_astar(
                self.state.player.position,
                self.state.pellets,
                self.state.maze,
                self.state.ghosts,
                self.state.player.position,
            )
            self.auto_path = path
        if self.auto_path and len(self.auto_path) > 1:
            # Advance one step along the path.
            for ghost in self.state.ghosts:
                if ghost.strategy_name == "A_STAR_AMBUSH":
                    ghost.extra["player_last_pos"] = self.state.player.position
            self.state.player.position = self.auto_path[1]
            self.auto_path = self.auto_path[1:]
