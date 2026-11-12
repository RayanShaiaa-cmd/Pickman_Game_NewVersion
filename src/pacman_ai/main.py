#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the Pac‑Man AI game.

Running ``python -m src.pacman_ai.main`` or executing ``run.py`` will start the
application.
"""

from .core.ui import choose_mode, choose_map, choose_difficulty, show_end_screen
from .core.game import GameManager


def main() -> None:
    """Main loop that asks the player for settings and starts the game.

    The function never returns – it either restarts the game (when the player
    selects *restart* on the end screen) or exits the process.
    """
    while True:
        mode_auto = choose_mode() == 1
        maze = choose_map()
        difficulty = choose_difficulty()  # currently unused but kept for API stability
        manager = GameManager(maze, difficulty, mode_auto)
        manager.run()
        # ``GameManager.run`` returns when the game ends. Convert ghosts to a simple
        # dict representation for the UI end screen.
        ghost_dicts = [g.as_dict() for g in manager.state.ghosts]
        if not show_end_screen(manager.state.score, manager.state.win, ghost_dicts):
            break


if __name__ == "__main__":
    main()
