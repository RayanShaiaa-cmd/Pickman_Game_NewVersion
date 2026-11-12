"""Core subpackage containing game engine, rendering, and UI utilities."""
import pygame

# Initialise pygame and its font module exactly once.
# This mirrors the original script’s behaviour but isolates the side‑effect.
pygame.init()          # sets up video, audio, and fonts
pygame.font.init()     # explicit font init for safety

# The rest of the core subpackage (game, renderer, ui) can now safely import
# pygame.font.SysFont and other pygame features.