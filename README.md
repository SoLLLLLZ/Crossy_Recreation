# Crossy Road Recreation

A recreation of the popular mobile game Crossy Road, built with Python and Pygame.

## Requirements

- Python 3.8+
- Pygame 2.5+

## Installation

```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

## Controls

- **Arrow Keys** or **WASD** - Move your character
- **ESC** - Pause the game

## Features (Stages)

- [x] Stage 1: Landing page with animated menu
- [ ] Stage 2: Character movement and basic terrain
- [ ] Stage 3: Infinite scrolling system
- [ ] Stage 4: Multiple terrain types
- [ ] Stage 5: Obstacles and collision detection
- [ ] Stage 6: Coins and scoring system
- [ ] Stage 7: Pause functionality and polish

## Project Structure

```
Crossy_Recreation/
├── main.py          # Entry point and game loop
├── menu.py          # Landing page and menu system
├── utils.py         # Constants and helper functions
├── player.py        # (Coming in Stage 2)
├── terrain.py       # (Coming in Stage 2)
├── obstacles.py     # (Coming in Stage 5)
├── coins.py         # (Coming in Stage 6)
└── game.py          # (Coming in Stage 2)
```

## Current Progress

**Stage 1 Complete** ✓
- Project structure initialized
- Animated landing page with floating decorations
- Interactive play button with hover effects
- Clean state management system
- Pygame setup and main game loop

## Next Steps

Stage 2 will add:
- Player character with grid-based movement
- Basic isometric terrain rendering
- Game state class