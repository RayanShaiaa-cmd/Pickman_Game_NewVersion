# Pac-Man AI

A modular, well‑engineered Pac‑Man clone with AI‑controlled ghosts and a player‑controlled Pac‑Man. The project demonstrates clean architecture, classic path‑finding algorithms (BFS, A*), predictive ghost strategies, and safe navigation for an AI player.

## Features

- **Modular codebase** – clear separation of core logic, AI, entities, maps, UI, and audio.
- **Multiple ghost personalities** – chaser (A*), ambusher (predictive), simpleton (BFS).
- **Three predefined maps** and a random maze generator.
- **Pellet collection**, scoring, win/loss conditions.
- **Sound effects** for win/lose.
- **Configurable** parameters (grid size, speeds, penalties, etc.).
- **Automated test suite** with `pytest` covering path‑finding, maze generation, and AI behavior.

## Installation

```bash
# Clone the repository
git clone <https://github.com/RayanShaiaa-cmd/Pickman_Game_NewVersion.git>
cd Folder_Name (When you clon the repo you will see the name)

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Game

```bash
python run.py
```

Use the menus to select player mode (manual or AI), map, and difficulty.

## Development

- Add new maps in `src/pacman_ai/maps/`.
- Implement new ghost strategies by extending `ai/strategies.py`.

## License

MIT License – see `LICENSE` for details.

## Author
Rayan Ebrahim Ali Hadi Shaiaa
