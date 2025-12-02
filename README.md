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

## Controlls

- **WASD**: Horizontal moviment (front/left/back/right)
- **QE**: Vertical moviment (down/up)
- **Mouse**: Camera rotate
- **Left Click**: Select Star
- **ESC**: Exit Game

## Installation

1. Clone repository:
```bash
git clone https://github.com/Lakentio/universe-engine.git
cd universe-engine
```

2. install dependencies:
```bash
pip install -r requirements.txt
```

3. Execute game:
```bash
python run.py
```

## Seeds Personalized

The Universe Engine supports custom seeds to ensure consistency in universe generation. The same seed will always generate the same universe.

### Use of Seeds

```bash
# use default seed
python run.py

# Use personalized seeds
python run.py --seed "meu-universo-123"

# view example seeds
python run.py --list-seeds
```

### Example Seeds

- `meu-universo-123`
- `galaxia-andromeda`
- `sistema-solar-2024`
- `nebulosa-vermelha`
- `cluster-estelar`

## Hardware

I tested the program with the default settings in a machine with I3 3220, 8GB Ram and no dedicated graphics card, and i got 58-62 FPS. 

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

To contribute to the project(please do this, I am a horrible dev, this project contain a lot of IA code):

1. Fork the repository
2. Create a branch for your feature
3. Commit your changes
4. Open a Pull Request

## License

This project is under the MIT License. See the LICENSE file for more details.
