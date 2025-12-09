# Universe Engine

A procedural space exploration engine developed in Python with Pygame, optimized for performance and with a modern interface.

## Description

The Universe Engine is an advanced 3D engine that generates an infinite procedural universe with stars. The player can navigate through space using keyboard and mouse controls, with an intelligent optimization system and a modern interface.

## Features

- **Procedural star generation** with custom seeds
- **Fluid 3D navigation** with keyboard and mouse controls
- **Optimized chunk system** for maximum performance
- **Frustum Culling** for efficient rendering
- **Modern interface** with transparent panels and gradients
- **Interactive minimap** of nearby stars
- **Performance system** with real-time statistics
- **Star selection** with detailed information
- **Distance fade** for realistic visual effect

## Controls

- **WASD**: Horizontal movement (front/left/back/right)
- **QE**: Vertical movement (down/up)
- **Mouse**: Camera rotate
- **Left Click**: Select Star
- **ESC**: Exit Game
- **F5**: Quick Save
- **F9**: Load Latest Save
- **F8**: List Saves in the logger
- **F6**: Open a menu to save the state

## Installation

1. Clone repository:
```bash
git clone https://github.com/Lakentio/universe-engine.git
cd universe-engine
```

2. (Optional but recommended) create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python run.py
```

To see the command line options use:
```bash
python run.py --help
```

## Hardware

I tested the program with the default settings on a machine with I3 3220, 8GB RAM, and no dedicated graphics card, and I got 58-62 FPS. 

## Project Structure

```
universe-engine/
├── src/
│   ├── main.py          # Main File of the project
│   │   ├── core/
│   │   │   ├── engine.py    # Main engine logic
│   │   │   └── __init__.py
│   │   ├── rendering/
│   │   │   ├── render.py    # Rendering and UI functions
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── config.py    # Game settings
│   │       └── __init__.py
│   ├── requirements.txt    # Python Dependencies
│   ├── .gitignore         # Ignored files for git
│   ├── run.py             # Runner Script
│   └── README.md          # Documentation
```
## Configuration

Game settings can be changed in the `src/utils/config.py` file:

### Basic Settings
- `WIDTH, HEIGHT`: Screen resolution
- `FOV_DEG`: Field of view in degrees
- `CHUNK_SIZE`: Size of each chunk
- `CHUNK_RADIUS`: Radius of visible chunks
- `STARS_PER_CHUNK`: Number of stars per chunk
- `MOVE_SPEED`: Movement speed
- `MOUSE_SENS`: Mouse sensitivity
- `TARGET_FPS`: Target FPS

### Seed Settings
- `GLOBAL_SEED`: Default seed for procedural generation
- `USE_CUSTOM_SEED`: Defines whether to use a custom seed
- `CUSTOM_SEED`: User's custom seed

### Performance Settings
- `FRUSTUM_CULLING`: Enables Frustum culling for optimization
- `MAX_VISIBLE_STARS`: Maximum limit of rendered stars
- `LOD_DISTANCE`: Distance to Level of Detail
- `STAR_FADE_DISTANCE`: Distance to fade stars

### UI/HUD Settings
- `UI_SCALE`: Interface scale
- `UI_COLORS`: Interface color palette
- `UI_FONT_SIZE`: Font size
- `UI_PANEL_ALPHA`: Panel transparency

## Development

If you want to contribute (very welcome!):

1. Fork the repository
2. Create a branch for your feature/bugfix
3. Run local tests and format the code
4. Open a Pull Request describing the change

Tips for beginners:
- Look for small files in `src/utils` or documentation improvements.
- Start by adding docstrings or small unit tests.
- If you prefer, ask a maintainer to mark an issue as "good first issue".

## License

This project is under the MIT License. See the LICENSE file for more details.

