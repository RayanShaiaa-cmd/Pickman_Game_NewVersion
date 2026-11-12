# Central configuration constants for the Pac‑Man AI project

# ---------------------------------------------------------------------------
# Core game settings
# ---------------------------------------------------------------------------
TILE: int = 24                      # Size of each square tile in pixels
ROWS: int = 30                      # Default number of rows in the grid
COLS: int = 30                      # Default number of columns in the grid
WIDTH: int = COLS * TILE            # Window width (computed)
HEIGHT: int = ROWS * TILE           # Window height (computed)
FPS: int = 5                        # Frames per second – can be increased for smoother play

# ---------------------------------------------------------------------------
# Colours – RGB tuples used by pygame
# ---------------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 230, 0)
BLUE = (0, 102, 204)
RED = (220, 20, 60)
PINK = (255, 105, 180)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# ---------------------------------------------------------------------------
# AI‑related parameters
# ---------------------------------------------------------------------------
PATH_PENALTY: int = 100_000          # Very high cost used to turn a cell into a "wall" for the safe‑navigator
PREDICTION_STEPS: int = 10          # Number of future steps we predict for each ghost
AMBUSH_DISTANCE: int = 4            # How many cells ahead of the player the ambusher aims for

# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------
# Sound files are expected to live in the project root (or assets/sounds)
WIN_SOUND_FILE = "win.wav"
LOSE_SOUND_FILE = "lose.wav"
