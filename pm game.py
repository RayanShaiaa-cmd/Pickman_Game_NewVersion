import pygame
import sys
import random
from collections import deque
import heapq
import math
import os
# محاولة استيراد numpy لتوليد أصوات احتياطية
try:
	import numpy as np
	HAS_NUMPY = True
except Exception:
	HAS_NUMPY = False

pygame.init()
pygame.mixer.init()

# ----- إعدادات عامة -----
TILE = 24
ROWS, COLS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
FPS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Multi Map (AI Predictive Avoidance - V3)")
clock = pygame.time.Clock()

# ----- ألوان -----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 230, 0)
BLUE = (0, 102, 204)
RED = (220, 20, 60)
PINK = (255, 105, 180)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

font = pygame.font.SysFont('Arial', 28, bold=True)
small_font = pygame.font.SysFont('Arial', 20)

# ----- خرائط (تم إبقاء الخرائط الأصلية) -----
MAPS = []
# Map 1
MAPS.append([
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
	[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
	[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1],
	[1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
	[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
	[1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
	[1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
	[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1],
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],])
# Map 2
MAPS.append([
	[1] * 30,
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
	[1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
	[1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
	[1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
	[1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],])
# Map 3
MAPS.append([
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
	[1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
	[1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
	[1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
	[1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
	[1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],])

def generate_random_maze(rows, cols):
	maze = [[1] * cols for _ in range(rows)]
	stack = [(1, 1)]
	maze[1][1] = 0
	while stack:
		current_r, current_c = stack[-1]
		unvisited_neighbors = []
		for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
			nr, nc = current_r + dr, current_c + dc
			if 0 < nr < rows - 1 and 0 < nc < cols - 1 and maze[nr][nc] == 1:
				unvisited_neighbors.append((nr, nc))
		if unvisited_neighbors:
			next_r, next_c = random.choice(unvisited_neighbors)
			maze[(current_r + next_r) // 2][(current_c + next_c) // 2] = 0
			maze[next_r][next_c] = 0
			stack.append((next_r, next_c))
		else:
			stack.pop()
	return maze
MAPS.append(generate_random_maze(ROWS, COLS))

# ----- دوال المسارات المعدلة (A* Custom) -----
def neighbors(cell, maze):
	r, c = cell
	ROWS = len(maze)
	COLS = len(maze[0])
	for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
		nr, nc = r + dr, c + dc
		if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
			yield (nr, nc)

def bfs_path(src, dst, maze):
	if src == dst: return [src]
	q = deque([src])
	prev = {src: None}
	visited = {src}  # يجب استخدام مجموعة للزيارات لتجنب الحلقات
	while q:
		cur = q.popleft()
		for nb in neighbors(cur, maze):
			if nb not in visited:
				visited.add(nb)
				prev[nb] = cur
				if nb == dst:
					path = [dst]
					while prev[path[-1]] is not None:
						path.append(prev[path[-1]])
					return path[::-1]
				q.append(nb)
	return None

def h_manhattan(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_custom_path(src, dst, maze, cost_func, heuristic_func=h_manhattan):
	# open_set stores (f_cost, g_cost, node)
	open_set = [(heuristic_func(src, dst), 0, src)]
	came = {src: None}
	g = {src: 0}
	closed = set()

	while open_set:
		f, cost, cur = heapq.heappop(open_set)
		if cur == dst:
			path = [cur]
			while came[path[-1]] is not None:
				path.append(came[path[-1]])
			return path[::-1]

		if cur in closed: continue
		closed.add(cur)
		# الحصول على مضاعف التكلفة للعقدة الحالية
		current_cost_multiplier = cost_func(cur)
		# إذا كانت التكلفة عالية جداً (عقوبة)، نتجاهل العقدة
		if current_cost_multiplier > 1000: continue
		for nb in neighbors(cur, maze):
			# استخدام مضاعف التكلفة للعقدة الهدف (nb) في حساب المسار الجديد (ng)
			# تم تعديل هذا السطر ليعكس مبدأ "تجنب العقدة التالية"
			next_cost_multiplier = cost_func(nb)
			ng = cost + next_cost_multiplier * 1
			if nb not in g or ng < g[nb]:
				g[nb] = ng
				f = ng + heuristic_func(nb, dst)
				heapq.heappush(open_set, (f, ng, nb))
				came[nb] = cur
	return None

def astar_path(src, dst, maze):
	return astar_custom_path(src, dst, maze, lambda n: 1)

# ----- أصوات الفوز/الخسارة (بقيت كما هي) -----
WIN_SOUND = None
LOSE_SOUND = None
def try_load_sounds():
	global WIN_SOUND, LOSE_SOUND
	try:
		if os.path.exists("win.wav"): WIN_SOUND = pygame.mixer.Sound("win.wav")
		if os.path.exists("lose.wav"): LOSE_SOUND = pygame.mixer.Sound("lose.wav")
		if WIN_SOUND or LOSE_SOUND: return
	except Exception:
		WIN_SOUND = LOSE_SOUND = None
	if HAS_NUMPY:
		try:
			def make_tone(freq=440, duration=0.4, volume=0.5):
				samplerate = 44100
				t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
				wave = (np.sin(2 * np.pi * freq * t) * (2 ** 15 - 1) * volume).astype(np.int16)
				stereo = np.column_stack([wave, wave])
				return pygame.sndarray.make_sound(stereo.copy())
			WIN_SOUND = make_tone(660, 0.35, 0.5)
			LOSE_SOUND = make_tone(220, 0.45, 0.6)
		except Exception:
			WIN_SOUND = LOSE_SOUND = None
try_load_sounds()
def play_win_sound():
	if WIN_SOUND: WIN_SOUND.play()
def play_lose_sound():
	if LOSE_SOUND: LOSE_SOUND.play()

# ----- شاشات الاختيار (بقيت كما هي) -----
def choose_mode():
	while True:
		screen.fill(BLACK)
		screen.blit(font.render("Choose Mode:", True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2 - 120))
		screen.blit(font.render("1 - Manual (You play)", True, WHITE), (WIDTH // 2 - 130, HEIGHT // 2 - 60))
		screen.blit(font.render("2 - Auto (AI plays)", True, WHITE), (WIDTH // 2 - 120, HEIGHT // 2))
		screen.blit(small_font.render("Use 1 or 2", True, GRAY), (WIDTH // 2 - 50, HEIGHT // 2 + 80))
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == pygame.QUIT: pygame.quit(); sys.exit()
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_1: return 0
				if e.key == pygame.K_2: return 1

def choose_map():
	map_names = ["Map 1", "Map 2", "Map 3", "Random Map"]
	while True:
		screen.fill(BLACK)
		title_text = font.render("Select a Map:", True, WHITE)
		screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 130))
		for i, name in enumerate(map_names):
			text = font.render(f"{i + 1} - {name}", True, WHITE)
			screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60 + i * 50))
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit();
				sys.exit()
			if e.type == pygame.KEYDOWN:
				if pygame.K_1 <= e.key <= pygame.K_4:
					map_index = e.key - pygame.K_1
					return MAPS[map_index]

def choose_difficulty():
	options_text = ["1 - Standard", "2 - Advanced", "3 - Expert"]
	while True:
		screen.fill(BLACK)
		screen.blit(font.render("Choose Game Setting (Ghosts are unique):", True, WHITE),
		            (WIDTH // 2 - 220, HEIGHT // 2 - 110))
		for i, opt in enumerate(options_text):
			screen.blit(font.render(opt, True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2 - 50 + i * 50))
		screen.blit(small_font.render("Ghosts now have fixed unique AIs.", True, GRAY),
		            (WIDTH // 2 - 130, HEIGHT // 2 + 120))
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == pygame.QUIT: pygame.quit(); sys.exit()
			if e.type == pygame.KEYDOWN and pygame.K_1 <= e.key <= pygame.K_3:
				return e.key - pygame.K_1

def show_end_screen(score, win=False, ghosts=[]):
	if win:
		play_win_sound()
	else:
		play_lose_sound()
	while True:
		screen.fill(BLACK)
		message = "You Win!" if win else "Game Over"
		color = GREEN if win else RED
		screen.blit(font.render(message, True, color), (WIDTH // 2 - 80, HEIGHT // 2 - 120))
		screen.blit(font.render(f"Final Score: {score}", True, WHITE), (WIDTH // 2 - 110, HEIGHT // 2 - 70))
		y_offset = HEIGHT // 2
		for i, g in enumerate(ghosts):
			name = g.get('name', f"Ghost {i + 1}")
			screen.blit(small_font.render(f"{name} moves: {g['moves']}", True, WHITE), (WIDTH // 2 - 80, y_offset))
			y_offset += 25
		screen.blit(small_font.render("Press R to Restart", True, WHITE), (WIDTH // 2 - 90, y_offset + 20))
		screen.blit(small_font.render("Press Q to Quit", True, WHITE), (WIDTH // 2 - 80, y_offset + 50))
		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == pygame.QUIT: pygame.quit(); sys.exit()
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_r: return True
				if e.key == pygame.K_q: return False

# ----- الذكاء الاصطناعي للاعب (AI Safe - A* مع تنبؤ فعّال) -----
def calculate_ambush_target(player_pos, last_player_pos, maze):
	ROWS, COLS = len(maze), len(maze[0])
	pr, pc = player_pos
	plr, plc = last_player_pos
	# حساب متجه الحركة
	dr, dc = (pr - plr), (pc - plc)

	# تحديد الهدف المتقدم (4 مربعات أمام اللاعب)
	ambush_target_r, ambush_target_c = pr + dr * 4, pc + dc * 4
	if (0 <= ambush_target_r < ROWS and
			0 <= ambush_target_c < COLS and
			maze[ambush_target_r][ambush_target_c] == 0):
		return (ambush_target_r, ambush_target_c)
	else:
		# العودة لموقع اللاعب الحالي إذا كان الكمين غير ممكن
		return player_pos

def predict_ghost_paths(player_pos, maze, ghosts):
	"""يتنبأ بالمسارات الخمس القادمة لكل شبح بناءً على استراتيجيتهم"""
	predicted_paths = {}
	steps = 10  # نتنبأ بـ 5 خطوات قادمة

	for i, g in enumerate(ghosts):
		pos = tuple(g['pos'])
		target = tuple(player_pos)
		strat = g['strategy']
		path = None

		if strat == "BFS_SIMPLE":
			full_path = bfs_path(pos, target, maze)
			if full_path: path = full_path[:steps + 1]

		elif strat == "A_STAR_DIRECT":
			full_path = astar_path(pos, target, maze)
			if full_path: path = full_path[:steps + 1]
		elif strat == "A_STAR_AMBUSH":
			# نحاكي تحديد هدف الكمين بدقة
			last_player_pos = g.get('player_last_pos', player_pos)
			ambush_target = calculate_ambush_target(player_pos, last_player_pos, maze)
			full_path = astar_path(pos, ambush_target, maze)
			if full_path: path = full_path[:steps + 1]
		# حفظ المسارات المتوقعة
		predicted_paths[g['name']] = set(path[1:]) if path and len(path) > 1 else set()
	return predicted_paths

def find_safe_path_astar(src, pellets, maze, ghosts, player_pos):
	"""يجد أقرب pellet مع تجنب مسارات الأشباح المتوقعة باستخدام A*"""

	# 1. التنبؤ بمسارات الأشباح وتحديد العقد المهددة
	predicted_paths = predict_ghost_paths(player_pos, maze, ghosts)
	all_threat_nodes = set()
	for path_set in predicted_paths.values():
		all_threat_nodes.update(path_set)
	# 2. تحديد هدف اللاعب (أقرب حبة)
	nearest_pellet = None
	bfs_q = deque([src])
	bfs_visited = {src}
	while bfs_q:
		cur = bfs_q.popleft()
		if cur in pellets:
			nearest_pellet = cur
			break
		for nb in neighbors(cur, maze):
			if nb not in bfs_visited:
				bfs_visited.add(nb)
				bfs_q.append(nb)

	if not nearest_pellet: return None
	# 3. بناء دالة التكلفة المضادة (Anti-Cost Function) - تم التعديل هنا
	PATH_PENALTY = 100000  # قيمة عالية جداً لتجنب المسارات المهددة (بمثابة جدار)

	def anti_ghost_cost(node):
		cost = 1  # التكلفة الأساسية للمرور بعقدة واحدة
		# **التجنب الاستباقي للمسارات المهددة:**
		if node in all_threat_nodes:
			# تجعل A* يتجنب هذا المسار تمامًا
			return PATH_PENALTY
			# **الابتعاد عن الأشباح القريبة (عقوبة القرب):**
		# إضافة عقوبة متناسبة مع القرب لمنع الاقتراب من الأشباح القريبة.
		for g in ghosts:
			dist = h_manhattan(node, tuple(g['pos']))
			# إذا كان الشبح قريباً جداً، زيادة التكلفة (مثلاً: 2 مربع أو أقل)
			if dist < 3:
				# كلما اقتربت المسافة، زادت التكلفة الإضافية
				# (مثلاً: 100 * 2 للمسافة 1، 100 * 1 للمسافة 2)
				cost += 100 * (3 - dist)
		return cost

	# 4. حساب المسار باستخدام A* المُعدلة
	path = astar_custom_path(src, nearest_pellet, maze, anti_ghost_cost)
	if path and len(path) > 1:
		return path
	else:
		# إذا لم يتم العثور على مسار آمن (بسبب العقوبات/الجدران)، نتحرك في اتجاه عشوائي آمن
		safe_moves = [n for n in neighbors(src, maze) if anti_ghost_cost(n) < PATH_PENALTY]
		if safe_moves:
			return [src, random.choice(safe_moves)]
		else:
			# في أسوأ الأحوال، نتحرك عشوائياً
			return [src, random.choice(list(neighbors(src, maze)))] if list(neighbors(src, maze)) else None

# ----- اللعبة الرئيسية (تم تعديل تحديث موقع اللاعب وحركة الأشباح) -----
def run_game(maze, difficulty, mode_auto):
	ROWS = len(maze)
	COLS = len(maze[0])
	pellets = {(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c] == 0}
	start = (1, 1)
	player = list(start)
	if start in pellets: pellets.remove(start)

	ghosts = [
		{"pos": [1, 26], "color": RED, "strategy": "A_STAR_DIRECT", "speed": 1, "cooldown": 0, "moves": 0, "name": "Chaser"},
		{"pos": [1, 27], "color": PINK, "strategy": "A_STAR_AMBUSH", "speed": 1, "cooldown": 0, "moves": 0, "name": "Ambusher", "player_last_pos": start},
		{"pos": [1, 28], "color": GREEN, "strategy": "BFS_SIMPLE", "speed": 1, "cooldown": 0, "moves": 0, "name": "Simpleton"},]
	score = 0
	over = False
	win = False
	tick = 0
	auto_path = None
	total_pellets = len(pellets) + 1

	while True:
		clock.tick(FPS)
		tick += 1
		for e in pygame.event.get():
			if e.type == pygame.QUIT: pygame.quit(); sys.exit()
			if e.type == pygame.KEYDOWN and not mode_auto:
				nr = nc = None
				if e.key == pygame.K_UP:
					nr, nc = player[0] - 1, player[1]
				elif e.key == pygame.K_DOWN:
					nr, nc = player[0] + 1, player[1]
				elif e.key == pygame.K_LEFT:
					nr, nc = player[0], player[1] - 1
				elif e.key == pygame.K_RIGHT:
					nr, nc = player[0], player[1] + 1
				if nr is not None and maze[nr][nc] == 0:
					player = [nr, nc]
		# AI Safe Move (اللاعب) - التجنب الاستباقي
		if mode_auto and not over and not win:
			if not auto_path or len(auto_path) <= 1:
				# 1. حساب المسار الآمن مع التنبؤ
				path_to_pellet = find_safe_path_astar(tuple(player), pellets, maze, ghosts, tuple(player))
				if path_to_pellet:
					auto_path = path_to_pellet
				else:
					auto_path = None
			if auto_path and len(auto_path) > 1:
				# 2. تحديث آخر موقع للاعب للشبح الوردي قبل أن يتحرك اللاعب
				for g in ghosts:
					if g['strategy'] == 'A_STAR_AMBUSH':
						g['player_last_pos'] = tuple(player)
				# 3. تحريك اللاعب إلى الخطوة التالية
				player = list(auto_path[1])
				auto_path = auto_path[1:]
		# جمع pellets
		if tuple(player) in pellets:
			pellets.remove(tuple(player))
			score += 10

		# تحقق فوز
		if not pellets:
			win = True
		collected = (total_pellets - len(pellets))
		progress = collected / total_pellets
		# حركة الأعداء وتطبيق استراتيجياتهم الفردية
		for g in ghosts:
			if g.get('cooldown', 0) > 0:
				g['cooldown'] -= 1
				continue
			g['cooldown'] = g.get('speed', 1) - 1
			pos = tuple(g['pos'])
			target = tuple(player)
			strat = g['strategy']
			next_pos = None
			# --- تطبيق الاستراتيجيات المختلفة للأشباح ---
			if strat == "BFS_SIMPLE":
				path = bfs_path(pos, target, maze)
				if path and len(path) > 1: next_pos = path[1]

			elif strat == "A_STAR_DIRECT":
				path = astar_path(pos, target, maze)
				if path and len(path) > 1: next_pos = path[1]
			elif strat == "A_STAR_AMBUSH":
				# يستخدم آخر موقع للاعب الذي تم تحديثه للتو
				last_player_pos = g.get('player_last_pos', player)
				ambush_target = calculate_ambush_target(target, last_player_pos, maze)
				path = astar_path(pos, ambush_target, maze)
				if path and len(path) > 1: next_pos = path[1]
			if next_pos:
				g['pos'] = [next_pos[0], next_pos[1]]
				g['moves'] += 1
		for g in ghosts:
			if tuple(g['pos']) == tuple(player):
				over = True
				break
		screen.fill(BLACK)
		for r in range(ROWS):
			for c in range(COLS):
				if maze[r][c] == 1: pygame.draw.rect(screen, BLUE, (c * TILE, r * TILE, TILE, TILE))
		for (r, c) in pellets: pygame.draw.circle(screen, WHITE, (c * TILE + TILE // 2, r * TILE + TILE // 2), 3)
		pygame.draw.circle(screen, YELLOW, (player[1] * TILE + TILE // 2, player[0] * TILE + TILE // 2), TILE // 2 - 2)
		for g in ghosts:
			pygame.draw.circle(screen, g['color'], (g['pos'][1] * TILE + TILE // 2, g['pos'][0] * TILE + TILE // 2),
			                   TILE // 2 - 2)
		screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
		mode_text = "Auto (A* Safe)" if mode_auto else "Manual"
		screen.blit(small_font.render(f"Mode: {mode_text}", True, GRAY), (WIDTH - 200, 10))
		screen.blit(small_font.render(f"G1 (Red): A* Direct", True, RED), (WIDTH - 200, 30))
		screen.blit(small_font.render(f"G2 (Pink): A* Ambush", True, PINK), (WIDTH - 200, 50))
		screen.blit(small_font.render(f"G3 (Green): BFS Simple", True, GREEN), (WIDTH - 200, 70))
		if over or win:
			if show_end_screen(score, win, ghosts):
				main()
			else:
				pygame.quit();
				sys.exit()

		pygame.display.flip()

# ----- main loop -----
def main():
	while True:
		mode_auto = choose_mode() == 1
		maze = choose_map()
		difficulty = choose_difficulty()
		run_game(maze, difficulty, mode_auto)

if __name__ == "__main__":
	main()