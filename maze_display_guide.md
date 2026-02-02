# Complete Guide: Terminal Maze Display with Curses

A step-by-step tutorial for building the display component of the A-Maze-ing project.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Get a Basic Grid Displaying](#step-1-get-a-basic-grid-displaying)
3. [Step 2: Add Colors](#step-2-add-colors)
4. [Step 3: Add the Menu](#step-3-add-the-menu)
5. [Step 4: Add Input Handling](#step-4-add-input-handling)
6. [Step 5: Test with Dummy Data](#step-5-test-with-dummy-data)
7. [Complete Working Code](#complete-working-code)
8. [Common Issues & Solutions](#common-issues--solutions)

---

## Prerequisites

### What You Need to Know

- Basic Python (loops, functions, classes)
- How to run Python scripts
- Basic terminal usage

### Install Curses (if needed)

Curses comes with Python on Linux/Mac. For Windows:

```bash
pip install windows-curses
```

### Understanding Curses Basics

**Key Concept:** Curses lets you control the terminal like a canvas.

```
Terminal = Grid of character cells
Each cell = 1 character + 1 color

   0   1   2   3   4   (columns)
0  [_][_][_][_][_]
1  [_][_][_][_][_]
2  [_][_][_][_][_]
   (rows)
```

**Important Methods:**
- `stdscr.addstr(y, x, text)` - Add text at position (row, column)
- `stdscr.refresh()` - Actually display what you added
- `stdscr.getch()` - Get a key press
- `stdscr.clear()` - Clear the screen

---

## Step 1: Get a Basic Grid Displaying

### Objective
Display a simple 5×5 grid of blocks on the screen.

### Concept

We'll use the `█` character (full block) to represent cells.

```
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
```

### Code: Version 1 - The Absolute Minimum

Create a file called `display_step1.py`:

```python
import curses

def main(stdscr):
    """Main function - curses gives us stdscr"""
    
    # Clear the screen
    stdscr.clear()
    
    # Draw a simple message
    stdscr.addstr(0, 0, "Hello from Curses!")
    
    # Actually show it (IMPORTANT!)
    stdscr.refresh()
    
    # Wait for a key press
    stdscr.getch()

# Run the program
curses.wrapper(main)
```

**Run it:**
```bash
python3 display_step1.py
```

**What happens:**
1. Terminal enters curses mode (looks different)
2. "Hello from Curses!" appears at top-left
3. Press any key to exit
4. Terminal returns to normal

**Understanding curses.wrapper():**
- Handles all the setup (initialization)
- Handles all the cleanup (restoration)
- Catches errors gracefully
- You just write your code in `main()`

---

### Code: Version 2 - Draw a Single Block

```python
import curses

def main(stdscr):
    stdscr.clear()
    
    # Draw a single block character
    stdscr.addstr(0, 0, "█")
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Try it!** You should see one █ character.

---

### Code: Version 3 - Draw a Row of Blocks

```python
import curses

def main(stdscr):
    stdscr.clear()
    
    # Draw 5 blocks in a row
    for x in range(5):
        stdscr.addstr(0, x * 2, "█")
        # x * 2 because █ is wide, we need spacing
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Output:**
```
█ █ █ █ █
```

**Why `x * 2`?**
The █ character is visually wide. Without spacing, they'd overlap. Try `x * 1` to see the difference!

---

### Code: Version 4 - Draw a 5×5 Grid

```python
import curses

def main(stdscr):
    stdscr.clear()
    
    # Grid size
    grid_width = 5
    grid_height = 5
    
    # Draw grid
    for y in range(grid_height):
        for x in range(grid_width):
            # Place block at position (y, x*2)
            stdscr.addstr(y, x * 2, "█")
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Output:**
```
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
```

**Success!** You have a basic grid!

---

### Exercise 1.1

Modify the code to:
1. Draw a 10×10 grid instead
2. Add a title "My Maze" above the grid
3. Add blank line between title and grid

**Hint:**
```python
stdscr.addstr(0, 0, "My Maze")
# Grid starts at row 2 (row 1 is blank)
for y in range(grid_height):
    stdscr.addstr(y + 2, x * 2, "█")
```

---

## Step 2: Add Colors

### Objective
Make different cells different colors (like entry, exit, walls).

### Understanding Color Pairs

Curses uses **color pairs**:
- Each pair = foreground color + background color
- You assign each pair a number
- Use that number when printing

**Available colors:**
- `curses.COLOR_BLACK`
- `curses.COLOR_RED`
- `curses.COLOR_GREEN`
- `curses.COLOR_YELLOW`
- `curses.COLOR_BLUE`
- `curses.COLOR_MAGENTA`
- `curses.COLOR_CYAN`
- `curses.COLOR_WHITE`

### Code: Version 1 - Single Colored Block

```python
import curses

def main(stdscr):
    stdscr.clear()
    
    # Step 1: Initialize colors
    curses.start_color()
    
    # Step 2: Define a color pair
    # Pair 1 = Red text on Black background
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Step 3: Use the color pair
    stdscr.addstr(0, 0, "█", curses.color_pair(1))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**You should see a red █!**

---

### Code: Version 2 - Multiple Colors

```python
import curses

def main(stdscr):
    stdscr.clear()
    curses.start_color()
    
    # Define multiple color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    # Use different colors
    stdscr.addstr(0, 0, "█", curses.color_pair(1))  # Red
    stdscr.addstr(0, 2, "█", curses.color_pair(2))  # Green
    stdscr.addstr(0, 4, "█", curses.color_pair(3))  # Yellow
    stdscr.addstr(0, 6, "█", curses.color_pair(4))  # Blue
    stdscr.addstr(0, 8, "█", curses.color_pair(5))  # Magenta
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Output:** A rainbow of blocks!

---

### Code: Version 3 - Grid with Different Colored Cells

```python
import curses

def main(stdscr):
    stdscr.clear()
    curses.start_color()
    
    # Define colors for maze elements
    COLOR_WALL = 1
    COLOR_ENTRY = 2
    COLOR_EXIT = 3
    
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ENTRY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(COLOR_EXIT, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Draw a 5×5 grid with special cells
    for y in range(5):
        for x in range(5):
            # Choose color based on position
            if x == 0 and y == 0:
                # Top-left = Entry (magenta)
                color = COLOR_ENTRY
            elif x == 4 and y == 4:
                # Bottom-right = Exit (red)
                color = COLOR_EXIT
            else:
                # Everything else = Wall (white)
                color = COLOR_WALL
            
            stdscr.addstr(y, x * 2, "█", curses.color_pair(color))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Output:**
- Top-left block is magenta (entry)
- Bottom-right block is red (exit)
- All others are white (walls)

**Success!** You now have colored cells!

---

### Exercise 2.1

Modify the code to:
1. Make the middle cell (2, 2) yellow
2. Make the entire first row green
3. Add a blue block at (3, 1)

---

## Step 3: Add the Menu

### Objective
Display a menu below the grid with options.

### Concept

We'll draw:
```
  A-Maze-ing

█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █
█ █ █ █ █

====================
1: Re-generate maze
2: Show/Hide path
3: Colour menu
4: Quit
====================
Choice (1-4): _
```

### Code: Version 1 - Title + Grid + Menu

```python
import curses

def main(stdscr):
    stdscr.clear()
    curses.start_color()
    
    # Colors
    COLOR_WALL = 1
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    # Title
    stdscr.addstr(0, 0, "  A-Maze-ing", curses.A_BOLD)
    
    # Grid (starting at row 2)
    grid_start_row = 2
    grid_height = 5
    grid_width = 5
    
    for y in range(grid_height):
        for x in range(grid_width):
            row = grid_start_row + y
            col = x * 2
            stdscr.addstr(row, col, "█", curses.color_pair(COLOR_WALL))
    
    # Menu (starting after grid + 1 blank line)
    menu_start_row = grid_start_row + grid_height + 1
    
    stdscr.addstr(menu_start_row, 0, "=" * 40)
    stdscr.addstr(menu_start_row + 1, 0, "1: Re-generate a new maze")
    stdscr.addstr(menu_start_row + 2, 0, "2: Show/Hide path from entry to exit")
    stdscr.addstr(menu_start_row + 3, 0, "3: Colour menu")
    stdscr.addstr(menu_start_row + 4, 0, "4: Quit")
    stdscr.addstr(menu_start_row + 5, 0, "=" * 40)
    stdscr.addstr(menu_start_row + 6, 0, "Choice (1-4): ")
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Success!** You now have a complete display with title, grid, and menu!

---

### Understanding Layout Calculation

```python
# Title at row 0
title_row = 0

# Blank line at row 1

# Grid starts at row 2
grid_start_row = 2
grid_height = 5
# Grid occupies rows 2-6 (5 rows total)

# Blank line at row 7

# Menu starts at row 8
menu_start_row = grid_start_row + grid_height + 1  # = 2 + 5 + 1 = 8
```

**Pro tip:** Always calculate positions based on previous sections. Don't hardcode row numbers!

---

### Exercise 3.1

Modify the code to:
1. Add your name below the title
2. Add a blank line between grid and menu
3. Add "Press Q to quit anytime" at the bottom

---

## Step 4: Add Input Handling

### Objective
Respond to user key presses (1, 2, 3, 4, q).

### Understanding getch()

```python
key = stdscr.getch()  # Waits for a key press
```

**Returns:** ASCII code of the pressed key
- Press 'a' → returns 97
- Press '1' → returns 49
- Press Enter → returns 10

**To check what was pressed:**
```python
if key == ord('1'):  # ord('1') converts '1' to its ASCII code (49)
    # User pressed 1
```

### Code: Version 1 - Detect a Single Key

```python
import curses

def main(stdscr):
    stdscr.clear()
    
    stdscr.addstr(0, 0, "Press any key...")
    stdscr.refresh()
    
    key = stdscr.getch()
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"You pressed key with ASCII code: {key}")
    stdscr.addstr(1, 0, f"Which is the character: '{chr(key)}'")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
```

**Try it:** Press different keys and see what codes they produce!

---

### Code: Version 2 - Simple Menu Loop

```python
import curses

def main(stdscr):
    while True:
        stdscr.clear()
        
        # Display menu
        stdscr.addstr(0, 0, "Menu:")
        stdscr.addstr(1, 0, "1: Option One")
        stdscr.addstr(2, 0, "2: Option Two")
        stdscr.addstr(3, 0, "Q: Quit")
        stdscr.addstr(5, 0, "Your choice: ")
        stdscr.refresh()
        
        # Get input
        key = stdscr.getch()
        
        # Handle input
        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr(0, 0, "You chose Option One!")
            stdscr.addstr(1, 0, "Press any key to continue...")
            stdscr.refresh()
            stdscr.getch()
        
        elif key == ord('2'):
            stdscr.clear()
            stdscr.addstr(0, 0, "You chose Option Two!")
            stdscr.addstr(1, 0, "Press any key to continue...")
            stdscr.refresh()
            stdscr.getch()
        
        elif key == ord('q') or key == ord('Q'):
            break  # Exit the loop

curses.wrapper(main)
```

**Try it:** Navigate the menu by pressing 1, 2, or Q!

---

### Code: Version 3 - Full Maze Display with Input

```python
import curses

def draw_display(stdscr, show_message=""):
    """Draw the complete display"""
    stdscr.clear()
    curses.start_color()
    
    # Colors
    COLOR_WALL = 1
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    # Title
    stdscr.addstr(0, 0, "  A-Maze-ing", curses.A_BOLD)
    
    # Grid
    grid_start = 2
    for y in range(5):
        for x in range(5):
            stdscr.addstr(grid_start + y, x * 2, "█", 
                         curses.color_pair(COLOR_WALL))
    
    # Menu
    menu_start = grid_start + 5 + 1
    stdscr.addstr(menu_start, 0, "=" * 40)
    stdscr.addstr(menu_start + 1, 0, "1: Re-generate a new maze")
    stdscr.addstr(menu_start + 2, 0, "2: Show/Hide path from entry to exit")
    stdscr.addstr(menu_start + 3, 0, "3: Colour menu")
    stdscr.addstr(menu_start + 4, 0, "4: Quit")
    stdscr.addstr(menu_start + 5, 0, "=" * 40)
    
    # Show message if any
    if show_message:
        stdscr.addstr(menu_start + 6, 0, show_message, curses.A_BOLD)
    
    stdscr.addstr(menu_start + 7, 0, "Choice (1-4): ")
    stdscr.refresh()

def main(stdscr):
    message = ""
    
    while True:
        draw_display(stdscr, message)
        message = ""  # Clear message after showing
        
        key = stdscr.getch()
        
        if key == ord('1'):
            message = "Generating new maze..."
            # TODO: Call maze generation
        
        elif key == ord('2'):
            message = "Path toggled!"
            # TODO: Toggle path visibility
        
        elif key == ord('3'):
            message = "Color menu (not implemented yet)"
            # TODO: Show color menu
        
        elif key == ord('4') or key == ord('q'):
            break

curses.wrapper(main)
```

**Success!** You now have a fully interactive display!

**Try pressing:**
- 1 → See "Generating new maze..." message
- 2 → See "Path toggled!" message
- 4 or Q → Exit

---

### Exercise 4.1

Add these features:
1. Make pressing ESC (key code 27) also quit
2. Show "Invalid choice!" if user presses anything else
3. Add a counter that shows how many times option 1 was pressed

---

## Step 5: Test with Dummy Data

### Objective
Test your display without needing the actual maze generator.

### Why This Matters

Your partner is working on maze generation. You need to test YOUR code NOW, not later!

**Solution:** Create fake/dummy maze data!

### Creating a Dummy Maze Class

```python
class DummyMaze:
    """Fake maze for testing display"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)
        
        # Create a simple grid (all cells have all walls for now)
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append('F')  # 'F' in hex = all walls
            self.grid.append(row)
    
    def cell_to_hex(self, x, y):
        """Return hex value for a cell"""
        return self.grid[y][x]
    
    def generate(self):
        """Fake generation - just changes some cells"""
        import random
        # Randomly change some cells
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = random.choice(['0', '3', '5', 'A', 'F'])
    
    def find_shortest_path(self):
        """Fake path - just a diagonal"""
        path = []
        for i in range(min(self.width, self.height)):
            path.append((i, i))
        return path
```

---

### Complete Test Program

```python
import curses
import random

class DummyMaze:
    """Fake maze for testing display"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)
        self.grid = [['F'] * width for _ in range(height)]
    
    def cell_to_hex(self, x, y):
        return self.grid[y][x]
    
    def generate(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = random.choice(['0', '3', '5', 'A', 'F'])
    
    def find_shortest_path(self):
        path = []
        for i in range(min(self.width, self.height)):
            path.append((i, i))
        return path


class MazeRenderer:
    """Display handler"""
    
    def __init__(self, maze):
        self.maze = maze
        self.show_path = False
        self.path_cells = []
        
        # Color IDs
        self.COLOR_WALL = 1
        self.COLOR_ENTRY = 2
        self.COLOR_EXIT = 3
        self.COLOR_PATH = 4
        self.COLOR_CLOSED = 5
    
    def setup_colors(self):
        curses.start_color()
        curses.init_pair(self.COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_ENTRY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_EXIT, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_PATH, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CLOSED, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    def get_cell_color(self, x, y):
        """Determine color for a cell"""
        if (x, y) == self.maze.entry:
            return self.COLOR_ENTRY
        if (x, y) == self.maze.exit:
            return self.COLOR_EXIT
        if self.show_path and (x, y) in self.path_cells:
            return self.COLOR_PATH
        
        hex_val = self.maze.cell_to_hex(x, y)
        if hex_val == 'F':
            return self.COLOR_CLOSED
        
        return self.COLOR_WALL
    
    def render(self, stdscr, message=""):
        """Draw everything"""
        stdscr.clear()
        
        # Title
        stdscr.addstr(0, 0, "  A-Maze-ing [TESTING MODE]", curses.A_BOLD)
        
        # Maze
        grid_row = 2
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                color = self.get_cell_color(x, y)
                stdscr.addstr(grid_row + y, x * 2, "█", 
                             curses.color_pair(color))
        
        # Menu
        menu_row = grid_row + self.maze.height + 1
        stdscr.addstr(menu_row, 0, "=" * 50)
        stdscr.addstr(menu_row + 1, 0, "1: Re-generate maze (random change)")
        stdscr.addstr(menu_row + 2, 0, "2: Show/Hide path (diagonal)")
        stdscr.addstr(menu_row + 3, 0, "3: Colour menu (not implemented)")
        stdscr.addstr(menu_row + 4, 0, "4: Quit")
        stdscr.addstr(menu_row + 5, 0, "=" * 50)
        
        if message:
            stdscr.addstr(menu_row + 6, 0, message, curses.A_BOLD)
        
        stdscr.addstr(menu_row + 7, 0, "Choice (1-4): ")
        stdscr.refresh()
    
    def run(self, stdscr):
        """Main loop"""
        self.setup_colors()
        message = ""
        
        while True:
            self.render(stdscr, message)
            message = ""
            
            key = stdscr.getch()
            
            if key == ord('1'):
                self.maze.generate()
                message = "✓ Maze regenerated!"
            
            elif key == ord('2'):
                self.show_path = not self.show_path
                if self.show_path:
                    self.path_cells = self.maze.find_shortest_path()
                message = f"✓ Path {'shown' if self.show_path else 'hidden'}!"
            
            elif key == ord('3'):
                message = "Color menu not yet implemented"
            
            elif key == ord('4') or key == ord('q'):
                break


# Test it!
def main(stdscr):
    # Create dummy 10×10 maze
    maze = DummyMaze(10, 10)
    
    # Create renderer
    renderer = MazeRenderer(maze)
    
    # Run it
    renderer.run(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
```

**Save this as `test_display.py` and run it!**

```bash
python3 test_display.py
```

**You should be able to:**
- See a 10×10 grid
- Press 1 to "regenerate" (cells change randomly)
- Press 2 to show/hide a diagonal path
- Press 4 to quit

**Success!** You can now develop your display independently!

---

### Testing Different Scenarios

**Test with different sizes:**
```python
maze = DummyMaze(20, 15)  # Your actual project size
```

**Test with different patterns:**
```python
def generate(self):
    # Make a checkerboard pattern
    for y in range(self.height):
        for x in range(self.width):
            if (x + y) % 2 == 0:
                self.grid[y][x] = 'F'  # Closed
            else:
                self.grid[y][x] = '0'  # Open
```

**Test edge cases:**
```python
maze = DummyMaze(3, 3)   # Very small
maze = DummyMaze(50, 50) # Very large
```

---

### Exercise 5.1

Modify DummyMaze to:
1. Create a border of 'F' cells around the edges
2. Make the "42" pattern visible (some 'F' cells in a pattern)
3. Create a more realistic path (not just diagonal)

---

## Complete Working Code

Here's everything put together in one complete, production-ready file:

```python
"""
Maze Display Module for A-Maze-ing Project
Handles terminal rendering using curses library
"""

import curses
from typing import List, Tuple


class MazeRenderer:
    """
    Terminal-based maze renderer using curses.
    
    Displays the maze with colors and handles user interaction.
    """
    
    def __init__(self, maze):
        """
        Initialize the renderer.
        
        Args:
            maze: Maze object with required methods:
                  - width, height properties
                  - entry, exit tuples
                  - cell_to_hex(x, y) method
                  - generate() method
                  - find_shortest_path() method
        """
        self.maze = maze
        self.show_path = False
        self.path_cells: List[Tuple[int, int]] = []
        
        # Color pair IDs
        self.COLOR_WALL = 1
        self.COLOR_ENTRY = 2
        self.COLOR_EXIT = 3
        self.COLOR_PATH = 4
        self.COLOR_CLOSED = 5
    
    def setup_colors(self) -> None:
        """Initialize curses color pairs."""
        curses.start_color()
        curses.init_pair(self.COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_ENTRY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_EXIT, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_PATH, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CLOSED, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    def get_cell_color(self, x: int, y: int) -> int:
        """
        Determine the color for a cell.
        
        Args:
            x: Column position
            y: Row position
            
        Returns:
            Color pair ID
        """
        # Check special positions first
        if (x, y) == self.maze.entry:
            return self.COLOR_ENTRY
        if (x, y) == self.maze.exit:
            return self.COLOR_EXIT
        if self.show_path and (x, y) in self.path_cells:
            return self.COLOR_PATH
        
        # Check if fully closed (for "42" pattern)
        hex_val = self.maze.cell_to_hex(x, y)
        if hex_val == 'F':
            return self.COLOR_CLOSED
        
        return self.COLOR_WALL
    
    def render(self, stdscr, message: str = "") -> None:
        """
        Render the complete display.
        
        Args:
            stdscr: Curses screen object
            message: Optional status message to display
        """
        stdscr.clear()
        
        # Title
        stdscr.addstr(0, 0, "  A-Maze-ing", curses.A_BOLD)
        
        # Draw maze grid
        grid_start_row = 2
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                color = self.get_cell_color(x, y)