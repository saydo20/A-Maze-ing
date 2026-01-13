# A-Maze-ing Project - Complete Guide for Beginners

## 📋 Table of Contents
1. [What is This Project?](#what-is-this-project)
2. [Core Concepts Explained](#core-concepts-explained)
3. [How the Program Works](#how-the-program-works)
4. [Task Division (2 People)](#task-division-2-people)
5. [Person 1: Detailed Tasks](#person-1-detailed-tasks)
6. [Person 2: Detailed Tasks](#person-2-detailed-tasks)
7. [Shared Tasks](#shared-tasks)
8. [Timeline & Milestones](#timeline--milestones)

---

## 🎮 What is This Project?

You're building a **maze generator program** in Python. Think of it like the software that creates mazes in video games or puzzle books.

### What Your Program Does:

```
INPUT (Config File)          PROCESS                OUTPUT
┌─────────────────┐         ┌──────────┐         ┌─────────────────┐
│ WIDTH=10        │  ────>  │  Maze    │  ────>  │ Hex File        │
│ HEIGHT=8        │         │Generator │         │ (encoded walls) │
│ ENTRY=0,0       │         └──────────┘         └─────────────────┘
│ EXIT=9,7        │                │
│ PERFECT=True    │                │
└─────────────────┘                ▼
                              ┌──────────┐
                              │ Visual   │
                              │ Display  │
                              └──────────┘
```

### The 4 Main Components:

1. **Configuration Parser** - Reads settings from a text file
2. **Maze Generator** - Creates the random maze using an algorithm
3. **File Writer** - Saves maze in hexadecimal format
4. **Visualizer** - Shows maze on screen with user interactions

---

## 🧩 Core Concepts Explained

### 1. What is a Maze Cell?

A maze is a grid of cells (like graph paper):

```
┌─────┬─────┬─────┐
│  1  │  2  │  3  │  ← Each square is a "cell"
├─────┼─────┼─────┤
│  4  │  5  │  6  │
├─────┼─────┼─────┤
│  7  │  8  │  9  │
└─────┴─────┴─────┘
```

Each cell has 4 possible walls:
- **North** (top)
- **East** (right) 
- **South** (bottom)
- **West** (left)

### 2. Wall Representation

Example of one cell with walls:

```
     North wall ✓
        ┌───┐
West ✗  │   │  East ✓
        └───┘
     South ✗
```

This cell has: North=YES, East=YES, South=NO, West=NO

### 3. Hexadecimal Encoding (IMPORTANT!)

Each cell's walls are encoded as ONE hexadecimal digit (0-F).

#### How It Works:

Each wall is represented by 1 bit:
- Bit 0 (value 1) = North wall
- Bit 1 (value 2) = East wall
- Bit 2 (value 4) = South wall
- Bit 3 (value 8) = West wall

If a wall exists, add its value:

**Example 1:** North + East walls
```
North (1) + East (2) = 3
Hex: 3
```

**Example 2:** All walls
```
North (1) + East (2) + South (4) + West (8) = 15
Hex: F
```

**Example 3:** Only South and West
```
South (4) + West (8) = 12
Hex: C
```

#### Complete Reference Table:

| Walls Present | Calculation | Hex | Visual |
|---------------|-------------|-----|--------|
| None | 0 | `0` | No walls |
| North | 1 | `1` | `┌─┐  ` |
| East | 2 | `2` | ` │` |
| North + East | 1+2=3 | `3` | `┌─┐│` |
| South | 4 | `4` | `└─┘` |
| North + South | 1+4=5 | `5` | `┌─┐└─┘` |
| East + South | 2+4=6 | `6` | ` │└─┘` |
| N + E + S | 1+2+4=7 | `7` | `┌─┐│└─┘` |
| West | 8 | `8` | `│ ` |
| North + West | 1+8=9 | `9` | `│┌─┐` |
| East + West | 2+8=10 | `A` | `│ │` |
| N + E + W | 1+2+8=11 | `B` | `│┌─┐│` |
| South + West | 4+8=12 | `C` | `│└─┘` |
| N + S + W | 1+4+8=13 | `D` | `│┌─┐└─┘` |
| E + S + W | 2+4+8=14 | `E` | `│ │└─┘` |
| All walls | 1+2+4+8=15 | `F` | `│┌─┐│└─┘` |

### 4. Perfect Maze Concept

A **perfect maze** has exactly ONE path between entry and exit:

```
PERFECT MAZE (only 1 path):     IMPERFECT MAZE (multiple paths):
┌───┬───┬───┐                   ┌───┬───┬───┐
│ E   * │   │                   │ E * * * * │
├───┤ * └───┤                   │ * ┴ * ┴ * │
│   │ * * * │                   │ * * * * X │
└───┴───┴─X─┘                   └───┴───┴───┘
```

---

## 🔄 How the Program Works

### Step-by-Step Flow:

```
1. User runs: python3 a_maze_ing.py config.txt
                    │
                    ▼
2. Program reads config.txt
   ┌────────────────────┐
   │ WIDTH=10           │
   │ HEIGHT=8           │
   │ ENTRY=0,0          │
   │ EXIT=9,7           │
   │ OUTPUT_FILE=maze.txt│
   │ PERFECT=True       │
   └────────────────────┘
                    │
                    ▼
3. Validate configuration
   - Is WIDTH > 0?
   - Is ENTRY inside maze?
   - Is EXIT inside maze?
   - Are ENTRY and EXIT different?
                    │
                    ▼
4. Generate maze using algorithm
   - Start with grid of cells
   - Use Recursive Backtracker (or Prim's/Kruskal's)
   - Remove walls to create paths
   - Ensure no 3×3 open areas
   - Add "42" pattern
   - If PERFECT=True, ensure single path
                    │
                    ▼
5. Find shortest path (BFS algorithm)
   - From ENTRY to EXIT
   - Record directions: N, E, S, W
                    │
                    ▼
6. Convert to hexadecimal
   - For each cell, encode walls as hex
   - Example: North+East walls = 3
                    │
                    ▼
7. Write to output file
   F8A3C...  ← Row 1
   3B5D9...  ← Row 2
   ...
   
   0,0       ← Entry
   9,7       ← Exit
   EESSNEES  ← Path
                    │
                    ▼
8. Display maze visually
   ┌───┬───┬───┐
   │ E * * │   │
   ├───┤ * ├───┤
   │   │ * * X │
   └───┴───┴───┘
                    │
                    ▼
9. User interactions
   - Press 'R' to regenerate
   - Press 'P' to show/hide path
   - Press 'C' to change colors
```

### Example Configuration File:

```bash
# Maze Configuration File
# Lines starting with # are comments

WIDTH=20          # Maze width in cells
HEIGHT=15         # Maze height in cells
ENTRY=0,0         # Entry coordinates (x,y)
EXIT=19,14        # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # Where to save the maze
PERFECT=True      # True = only one path, False = multiple paths
```

### Example Output File:

```
F8C4A2B3D5E6A1C3
3A5B9C7D2E4F6A8B
C4D5E6F7A8B9C1D2
...
[empty line]
0,0
19,14
EESSEENNEESSEENN
```

---

## 👥 Task Division (2 People)

### Overview:

```
┌─────────────────────────────────────────────────────────────┐
│                      PROJECT STRUCTURE                       │
├──────────────────────────┬──────────────────────────────────┤
│      PERSON 1            │           PERSON 2               │
│  Maze Generation Core    │    I/O & Visualization           │
├──────────────────────────┼──────────────────────────────────┤
│ • Algorithm Research     │ • Config File Parser             │
│ • MazeGenerator Class    │ • Input Validation               │
│ • Wall Logic             │ • Hex Encoding                   │
│ • Constraints            │ • Output File Writer             │
│ • "42" Pattern           │ • BFS Pathfinding                │
│ • Perfect Maze Logic     │ • Visual Display                 │
│ • Testing                │ • User Interactions              │
│                          │ • Python Package                 │
└──────────────────────────┴──────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Integration   │
                    │ (Both Work    │
                    │  Together)    │
                    └───────────────┘
```

### Why This Division is Fair:

**Person 1 (Algorithm):**
- Fewer tasks but more complex
- Requires deep algorithmic thinking
- Core "brain" of the project
- ~40% of total work

**Person 2 (I/O & Display):**
- More tasks but smaller pieces
- More variety in types of work
- Deals with user-facing features
- ~45% of total work

**Both Together:**
- ~15% shared integration work

---

