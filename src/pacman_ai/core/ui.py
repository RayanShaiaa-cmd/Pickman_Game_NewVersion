"""UI helper functions for mode, map, difficulty selection and end screen.

All functions use the globally‑initialised pygame ``screen`` and fonts from
``pacman_ai.core.renderer``. They are pure UI – no game state is modified here
except for returning the user's choice.
"""

import pygame
from ..config import settings
from ..maps import predefined, generator
from ..audio.sound_manager import play_win_sound, play_lose_sound
from .renderer import screen, font, small_font


def choose_mode() -> int:
    """Prompt the player to select Manual (0) or AI Auto (1) mode.

    Returns ``0`` for manual control, ``1`` for AI‑controlled player.
    """
    while True:
        screen.fill(settings.BLACK)
        screen.blit(font.render("Choose Mode:", True, settings.WHITE), (settings.WIDTH // 2 - 100, settings.HEIGHT // 2 - 120))
        screen.blit(font.render("1 - Manual (You play)", True, settings.WHITE), (settings.WIDTH // 2 - 130, settings.HEIGHT // 2 - 60))
        screen.blit(font.render("2 - Auto (AI plays)", True, settings.WHITE), (settings.WIDTH // 2 - 120, settings.HEIGHT // 2))
        screen.blit(small_font.render("Use 1 or 2", True, settings.GRAY), (settings.WIDTH // 2 - 50, settings.HEIGHT // 2 + 80))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    return 0
                if e.key == pygame.K_2:
                    return 1


def choose_map():
    """Let the user pick a map.

    Returns a **new** maze list (so that the random map does not mutate the
    original constant data).
    """
    map_names = ["Map 1", "Map 2", "Map 3", "Random Map"]
    while True:
        screen.fill(settings.BLACK)
        title = font.render("Select a Map:", True, settings.WHITE)
        screen.blit(title, (settings.WIDTH // 2 - title.get_width() // 2, settings.HEIGHT // 2 - 130))
        for i, name in enumerate(map_names):
            txt = font.render(f"{i + 1} - {name}", True, settings.WHITE)
            screen.blit(txt, (settings.WIDTH // 2 - txt.get_width() // 2, settings.HEIGHT // 2 - 60 + i * 50))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN and pygame.K_1 <= e.key <= pygame.K_4:
                idx = e.key - pygame.K_1
                if idx == 3:  # Random map
                    return generator.generate_random_maze(settings.ROWS, settings.COLS)
                return predefined.MAPS[idx]


def choose_difficulty() -> int:
    """Select a difficulty level (currently unused but kept for API compatibility)."""
    options = ["1 - Standard", "2 - Advanced", "3 - Expert"]
    while True:
        screen.fill(settings.BLACK)
        screen.blit(
            font.render("Choose Game Setting (Ghosts are unique):", True, settings.WHITE),
            (settings.WIDTH // 2 - 220, settings.HEIGHT // 2 - 110),
        )
        for i, opt in enumerate(options):
            screen.blit(font.render(opt, True, settings.WHITE), (settings.WIDTH // 2 - 100, settings.HEIGHT // 2 - 50 + i * 50))
        screen.blit(
            small_font.render("Ghosts now have fixed unique AIs.", True, settings.GRAY),
            (settings.WIDTH // 2 - 130, settings.HEIGHT // 2 + 120),
        )
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN and pygame.K_1 <= e.key <= pygame.K_3:
                return e.key - pygame.K_1


def show_end_screen(score: int, win: bool, ghosts) -> bool:
    """Display win/lose screen and return ``True`` to restart, ``False`` to quit.

    ``ghosts`` is a list of :class:`Ghost` objects – the function shows each
    ghost's name and move count.
    """
    if win:
        play_win_sound()
    else:
        play_lose_sound()
    while True:
        screen.fill(settings.BLACK)
        message = "You Win!" if win else "Game Over"
        color = settings.GREEN if win else settings.RED
        screen.blit(font.render(message, True, color), (settings.WIDTH // 2 - 80, settings.HEIGHT // 2 - 120))
        screen.blit(font.render(f"Final Score: {score}", True, settings.WHITE), (settings.WIDTH // 2 - 110, settings.HEIGHT // 2 - 70))
        y = settings.HEIGHT // 2
        for i, g in enumerate(ghosts):
            name = g.get('name', f"Ghost {i + 1}")
            screen.blit(
                small_font.render(f"{name} moves: {g['moves']}", True, settings.WHITE),
                (settings.WIDTH // 2 - 80, y),
            )
            y += 25
        screen.blit(small_font.render("Press R to Restart", True, settings.WHITE), (settings.WIDTH // 2 - 90, y + 20))
        screen.blit(small_font.render("Press Q to Quit", True, settings.WHITE), (settings.WIDTH // 2 - 80, y + 50))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_q:
                    return False
