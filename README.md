*This project has been created as part of the 42 curriculum by sjdia, ymouafak.*

---

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and visualizer built in Python. The goal of the project is to generate random mazes, display them either in the terminal or in a graphical window, and provide an interactive experience including pathfinding, animations, and a player mode.

The program reads a configuration file to set the maze parameters, generates a maze using the **Depth-First Search (DFS)** algorithm, finds the shortest path using **Breadth-First Search (BFS)**, and renders everything visually with an interactive interface built using the `curses` library.

Key features include:
- Random maze generation with an optional seed for reproducibility
- The '42' pattern embedded in the maze
- Shortest path visualization
- Maze generation and pathfinding animations
- A player mode to navigate the maze manually
- A reusable Python package (`mazegen`) for the core logic

---

## Instructions

### Requirements

- Python 3.10 or higher
- A terminal that supports `curses` (Linux / macOS)

### Running the program directly

```bash
python3 a_maze_ing.py config.txt
```

### Installing the reusable package

You can install the maze generator module using pip:

```bash
pip install mazegen_a_maze_ing-1.0.0-py3-none-any.whl
```

Or rebuild it from source:

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install build tools
pip install build

# Build the package
python -m build

# Install the built package
pip install dist/mazegen_a_maze_ing-1.0.0-py3-none-any.whl

# Run the program
python3 a_maze_ing.py config.txt
```

### Interactive Controls

| Key | Action |
|-----|--------|
| `R` | Regenerate a new maze |
| `S` | Show / Hide the shortest path |
| `C` | Change wall colors |
| `P` | Toggle player mode |
| `Q` | Quit the program |

---

## Configuration File

The configuration file uses a simple `KEY=VALUE` format. Lines starting with `#` are treated as comments.

### Example

```
WIDTH=19
HEIGHT=15
ENTRY=1,1
EXIT=4,4
OUTPUT_FILE=maze.txt
PERFECT=true
SEED=None
```

### Keys

| Key | Type | Description |
|-----|------|-------------|
| `WIDTH` | int | Width of the maze (number of columns) |
| `HEIGHT` | int | Height of the maze (number of rows) |
| `ENTRY` | int tuple | Entry point of the maze, format: `row,col` |
| `EXIT` | int tuple | Exit point of the maze, format: `row,col` |
| `OUTPUT_FILE` | string | Path to the output file where the maze is saved |
| `PERFECT` | bool | If `true`, generates a perfect maze (exactly one path between any two cells) |
| `SEED` | not None | Seed for random generation. Use `None` for a random maze each time |

### Rules

- Comment lines start with `#`
- Each line follows the `KEY=VALUE` format
- `PERFECT` accepts `true` or `false`
- `ENTRY` and `EXIT` must be valid coordinates within the maze bounds
- `SEED` must be an integer or something except `None`

---

## Maze Generation Algorithm

### Generation — Depth-First Search (DFS)

The maze is generated using the **Recursive Backtracker** algorithm, which is based on DFS. Starting from the entry cell, the algorithm visits neighbors randomly, carves a path through unvisited cells, and backtracks when it reaches a dead end. This produces mazes with long, winding corridors and a natural feel.

**Why DFS?**
- Simple to implement and understand
- Produces visually interesting and complex mazes
- Guarantees a perfect maze (every cell reachable, exactly one path between any two cells) when `PERFECT=true`
- Easy to animate step by step

### Pathfinding — Breadth-First Search (BFS)

The shortest path from entry to exit is found using **BFS**. Starting from the entry point, BFS explores all neighboring cells level by level, guaranteeing that the first time it reaches the exit, it has found the shortest path.

---

## Reusable Module

The core logic of the project is packaged as a reusable Python module called `mazegen`. It contains three submodules:

| Module | Description |
|--------|-------------|
| `mazegen.maze_generation` | DFS maze generation and BFS pathfinding logic |
| `mazegen.maze_drawing` | Visual rendering using `curses`, animations, banner |
| `mazegen.banner` | a banner to use in other projects|
| `mazegen.parsing` | Configuration file parsing and validation |

### How to use it

```bash
make run
```

---

## Bonuses

- **Maze generation animation** — Watch the maze being built step by step
- **Pathfinding animation** — Watch BFS explore the maze to find the shortest path
- **Banner** — A visual banner displayed at the start of the program
- **Player mode** — Navigate through the maze manually using keyboard controls

---

## Team and Project Management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| `sjdia` | Maze generation (DFS), pathfinding (BFS), parsing, banner, packaging |
| `ymouafak` | Maze drawing, visual representation, curses interface |


### Tools used

- **VSCode** — Code editor
- **Git / GitHub** — Version control and collaboration
- **Python `curses`** — Terminal-based graphical interface
- **`setuptools` + `build` + `venv`** — Python packaging

---

## Resources

- [Real Python](https://realpython.com) — Python tutorials and guides
- [GeeksForGeeks](https://www.geeksforgeeks.org) — Algorithm explanations (DFS, BFS)
- [Python `curses` documentation](https://docs.python.org/3/library/curses.html) — Official curses library docs
- [Python Packaging User Guide](https://packaging.python.org) — Guide on building and distributing Python packages
- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Overview of maze generation techniques

### AI Usage

AI (Claude) was used during this project for the following tasks:
- Explaining the **DFS** and **BFS** algorithms and how to apply them to maze generation and pathfinding
- Explaining new Python concepts encountered during development
- Explaining how to work with the **`curses`** library and how to draw in the terminal using it
- Helping understand and set up the **Python packaging** process (`pyproject.toml`, build tools, relative imports)