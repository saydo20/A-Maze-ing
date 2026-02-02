import curses
import sys
import time
import ast

TOP = 1
RIGHT = 2
BOTTOM = 4
LEFT = 8

# ================= COLOR SCHEMES =================

COLOR_SCHEMES = {
    "classic": {
        "wall": curses.COLOR_RED,
        "path": curses.COLOR_RED,
        "player": curses.COLOR_YELLOW,
        "markers": curses.COLOR_CYAN,
        "grid": curses.COLOR_WHITE
    },
    "ocean": {
        "wall": curses.COLOR_BLUE,
        "path": curses.COLOR_CYAN,
        "player": curses.COLOR_YELLOW,
        "markers": curses.COLOR_WHITE,
        "grid": curses.COLOR_BLUE
    },
    "forest": {
        "wall": curses.COLOR_GREEN,
        "path": curses.COLOR_YELLOW,
        "player": curses.COLOR_RED,
        "markers": curses.COLOR_WHITE,
        "grid": curses.COLOR_GREEN
    },
    "sunset": {
        "wall": curses.COLOR_MAGENTA,
        "path": curses.COLOR_YELLOW,
        "player": curses.COLOR_RED,
        "markers": curses.COLOR_WHITE,
        "grid": curses.COLOR_MAGENTA
    },
    "mono": {
        "wall": curses.COLOR_WHITE,
        "path": curses.COLOR_WHITE,
        "player": curses.COLOR_WHITE,
        "markers": curses.COLOR_WHITE,
        "grid": curses.COLOR_WHITE
    }
}

CURRENT_SCHEME = "classic"

# ================= FILE PARSER =================

def read_file(path):
    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    maze_lines = []
    i = 0

    while i < len(lines) and all(c in "0123456789ABCDEFabcdef" for c in lines[i]):
        maze_lines.append(lines[i])
        i += 1

    maze = [[int(c, 16) for c in line] for line in maze_lines]

    entry = ast.literal_eval(lines[i]); i += 1
    exit_  = ast.literal_eval(lines[i]); i += 1
    path = lines[i]

    return maze, entry, exit_, path

# ================= SAFE DRAW =================

def safe_addch(stdscr, y, x, ch, color=0, offset_y=0, offset_x=0):
    H, W = stdscr.getmaxyx()
    actual_y = y + offset_y
    actual_x = x + offset_x
    if 0 <= actual_y < H and 0 <= actual_x < W:
        try:
            if color:
                stdscr.attron(curses.color_pair(color))
            stdscr.addch(actual_y, actual_x, ch)
            if color:
                stdscr.attroff(curses.color_pair(color))
        except:
            pass

def safe_addstr(stdscr, y, x, text, color=0):
    H, W = stdscr.getmaxyx()
    if 0 <= y < H and 0 <= x < W:
        try:
            max_len = W - x - 1
            if max_len > 0:
                if color:
                    stdscr.attron(curses.color_pair(color))
                stdscr.addstr(y, x, text[:max_len])
                if color:
                    stdscr.attroff(curses.color_pair(color))
        except:
            pass

# ================= WALL CHARS =================

def wall_char(up, right, down, left):
    mask = (up << 0) | (right << 1) | (down << 2) | (left << 3)
    table = {
        0b0000: " ",
        0b0001: "╹",
        0b0010: "╺",
        0b0011: "┗",
        0b0100: "╻",
        0b0101: "┃",
        0b0110: "┏",
        0b0111: "┣",
        0b1000: "╸",
        0b1001: "┛",
        0b1010: "━",
        0b1011: "┻",
        0b1100: "┓",
        0b1101: "┫",
        0b1110: "┳",
        0b1111: "╋",
    }
    return table[mask]

# ================= BUILD WALL GRID =================

def set_wall(grid, y, x, is_red):
    if grid[y][x] == 1:
        return
    grid[y][x] = 1 if is_red else 0

def build_wall_grid(maze):
    h = len(maze)
    w = len(maze[0])

    grid = [[None for _ in range(w * 2 + 1)] for _ in range(h * 2 + 1)]

    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            gy = y * 2
            gx = x * 2

            is_closed = (cell == 15)  # F

            if cell & TOP:
                for i in range(3):
                    set_wall(grid, gy, gx + i, is_closed)

            if cell & BOTTOM:
                for i in range(3):
                    set_wall(grid, gy + 2, gx + i, is_closed)

            if cell & LEFT:
                for i in range(3):
                    set_wall(grid, gy + i, gx, is_closed)

            if cell & RIGHT:
                for i in range(3):
                    set_wall(grid, gy + i, gx + 2, is_closed)

    return grid

# ================= CALCULATE OFFSETS =================

def calculate_offsets(stdscr, grid):
    H, W = stdscr.getmaxyx()
    grid_h = len(grid)
    grid_w = len(grid[0])
    
    offset_y = max(0, (H - grid_h - 6) // 2)
    offset_x = max(0, (W - grid_w) // 2)
    
    return offset_y, offset_x

# ================= ANIMATE MAZE GENERATION =================

def animate_maze_generation(stdscr, maze, grid, offset_y, offset_x):
    """Animate the maze appearing with a smooth grid effect"""
    h = len(maze)
    w = len(maze[0])
    
    # Draw complete grid frame by frame
    for y in range(h + 1):
        for x in range(w + 1):
            gy = y * 2
            gx = x * 2
            
            # Draw corners
            if y <= h and x <= w:
                safe_addch(stdscr, gy, gx, "┼", 5, offset_y, offset_x)
            
            # Draw horizontal lines
            if x < w and y <= h:
                safe_addch(stdscr, gy, gx + 1, "─", 5, offset_y, offset_x)
            
            # Draw vertical lines  
            if y < h and x <= w:
                safe_addch(stdscr, gy + 1, gx, "│", 5, offset_y, offset_x)
        
        stdscr.refresh()
        time.sleep(0.02)
    
    time.sleep(0.3)
    
    # Now remove walls to reveal the maze
    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            gy = y * 2
            gx = x * 2
            
            # Clear passages (where there are NO walls)
            if not (cell & TOP):
                safe_addch(stdscr, gy, gx + 1, " ", 0, offset_y, offset_x)
            
            if not (cell & BOTTOM):
                safe_addch(stdscr, gy + 2, gx + 1, " ", 0, offset_y, offset_x)
            
            if not (cell & LEFT):
                safe_addch(stdscr, gy + 1, gx, " ", 0, offset_y, offset_x)
            
            if not (cell & RIGHT):
                safe_addch(stdscr, gy + 1, gx + 2, " ", 0, offset_y, offset_x)
        
        if y % 2 == 0:
            stdscr.refresh()
            time.sleep(0.02)
    
    time.sleep(0.2)
    
    # Draw final clean maze
    draw_maze(stdscr, grid, offset_y, offset_x)
    stdscr.refresh()

# ================= DRAW MAZE =================

def draw_maze(stdscr, grid, offset_y, offset_x):
    H = len(grid)
    W = len(grid[0])

    for y in range(H):
        for x in range(W):
            if grid[y][x] is None:
                safe_addch(stdscr, y, x, " ", 0, offset_y, offset_x)
            else:
                up = y > 0 and grid[y-1][x] is not None
                down = y < H-1 and grid[y+1][x] is not None
                left = x > 0 and grid[y][x-1] is not None
                right = x < W-1 and grid[y][x+1] is not None

                ch = wall_char(up, right, down, left)
                color = 1 if grid[y][x] == 1 else 0
                safe_addch(stdscr, y, x, ch, color, offset_y, offset_x)

# ================= ANIMATE PATH WITH FILLED BLOCKS =================

def animate_path(stdscr, grid, entry, exit_, path, offset_y, offset_x, show_player=True):
    sy = entry[0] * 2 + 1
    sx = entry[1] * 2 + 1
    ey = exit_[0] * 2 + 1
    ex = exit_[1] * 2 + 1

    # Draw start marker
    safe_addch(stdscr, sy, sx, "S", 4, offset_y, offset_x)
    stdscr.refresh()
    time.sleep(0.4)

    DIR = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

    cy, cx = sy, sx
    
    # Animate the path with filled blocks
    for move in path:
        dy, dx = DIR[move]
        
        # Move two steps (one cell) with filled blocks
        for step in range(2):
            cy += dy
            cx += dx
            
            # Don't overwrite start or end markers
            if (cy, cx) == (sy, sx) or (cy, cx) == (ey, ex):
                continue
            
            # Draw filled block for path
            safe_addch(stdscr, cy, cx, "█", 2, offset_y, offset_x)
            
            if show_player:
                stdscr.refresh()
                time.sleep(0.025)

    # Draw end marker
    safe_addch(stdscr, ey, ex, "E", 4, offset_y, offset_x)
    
    if show_player:
        stdscr.refresh()
        time.sleep(0.2)
        # Draw player at end
        safe_addch(stdscr, ey, ex, "X", 3, offset_y, offset_x)
    
    stdscr.refresh()

# ================= DRAW CONTROLS =================

def draw_controls(stdscr, current_scheme):
    H, W = stdscr.getmaxyx()
    controls = [
        "╔════════════════════════════╗",
        "║ R - Replay Animation       ║",
        "║ C - Change Color Scheme    ║",
        "║ Q/ESC - Exit              ║",
        f"║ Theme: {current_scheme.capitalize():<18} ║",
        "╚════════════════════════════╝"
    ]
    
    start_y = H - len(controls) - 1
    start_x = 2
    
    for i, text in enumerate(controls):
        safe_addstr(stdscr, start_y + i, start_x, text)

# ================= DRAW TITLE =================

def draw_title(stdscr):
    title = "╔═══════════════════════╗"
    text =  "║    MAZE NAVIGATOR     ║"
    bottom ="╚═══════════════════════╝"
    
    safe_addstr(stdscr, 0, 2, title, 4)
    safe_addstr(stdscr, 1, 2, text, 4)
    safe_addstr(stdscr, 2, 2, bottom, 4)

# ================= INIT COLORS =================

def init_colors(scheme_name):
    global CURRENT_SCHEME
    CURRENT_SCHEME = scheme_name
    scheme = COLOR_SCHEMES[scheme_name]
    
    curses.init_pair(1, scheme["wall"], -1)
    curses.init_pair(2, scheme["path"], -1)
    curses.init_pair(3, scheme["player"], -1)
    curses.init_pair(4, scheme["markers"], -1)
    curses.init_pair(5, scheme["grid"], -1)

# ================= MAIN =================

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    curses.start_color()
    curses.use_default_colors()
    
    if len(sys.argv) != 2:
        stdscr.addstr(0, 0, "Usage: python3 maze.py maze.txt")
        stdscr.getch()
        return

    maze, entry, exit_, path = read_file(sys.argv[1])
    grid = build_wall_grid(maze)
    
    scheme_names = list(COLOR_SCHEMES.keys())
    scheme_idx = 0
    init_colors(scheme_names[scheme_idx])
    
    offset_y, offset_x = calculate_offsets(stdscr, grid)
    
    # Draw title
    draw_title(stdscr)
    draw_controls(stdscr, CURRENT_SCHEME)
    stdscr.refresh()
    time.sleep(0.5)
    
    # Animate maze generation
    animate_maze_generation(stdscr, maze, grid, offset_y, offset_x)
    
    # Animate path
    animate_path(stdscr, grid, entry, exit_, path, offset_y, offset_x, show_player=True)
    
    while True:
        draw_controls(stdscr, CURRENT_SCHEME)
        stdscr.refresh()
        
        try:
            key = stdscr.getch()
        except:
            continue
        
        if key in (ord('q'), ord('Q'), 27):  # Q or ESC
            break
        elif key in (ord('r'), ord('R')):  # Replay
            stdscr.clear()
            draw_title(stdscr)
            draw_controls(stdscr, CURRENT_SCHEME)
            animate_maze_generation(stdscr, maze, grid, offset_y, offset_x)
            animate_path(stdscr, grid, entry, exit_, path, offset_y, offset_x, show_player=True)
        elif key in (ord('c'), ord('C')):  # Change color
            scheme_idx = (scheme_idx + 1) % len(scheme_names)
            init_colors(scheme_names[scheme_idx])
            stdscr.clear()
            draw_title(stdscr)
            draw_controls(stdscr, CURRENT_SCHEME)
            draw_maze(stdscr, grid, offset_y, offset_x)
            animate_path(stdscr, grid, entry, exit_, path, offset_y, offset_x, show_player=False)
            ey = exit_[0] * 2 + 1
            ex = exit_[1] * 2 + 1
            safe_addch(stdscr, ey, ex, "X", 3, offset_y, offset_x)

if __name__ == "__main__":
    curses.wrapper(main)