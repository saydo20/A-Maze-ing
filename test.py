import curses
import sys

TOP = 1
RIGHT = 2
BOTTOM = 4
LEFT = 8

def read_maze(path):
    maze = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            maze.append([int(c, 16) for c in line])
    return maze

def wall_char(up, right, down, left):
    # Build mask with correct bit positions: UP=0, RIGHT=1, DOWN=2, LEFT=3
    mask = (up << 0) | (right << 1) | (down << 2) | (left << 3)
    table = {
        0b0000: " ",
        0b0001: "╹",  # up only
        0b0010: "╺",  # right only
        0b0011: "┗",  # up + right
        0b0100: "╻",  # down only
        0b0101: "┃",  # up + down
        0b0110: "┏",  # right + down
        0b0111: "┣",  # up + right + down
        0b1000: "╸",  # left only
        0b1001: "┛",  # up + left
        0b1010: "━",  # right + left
        0b1011: "┻",  # up + right + left
        0b1100: "┓",  # down + left
        0b1101: "┫",  # up + down + left
        0b1110: "┳",  # right + down + left
        0b1111: "╋",  # all four
    }
    return table[mask]

def draw_maze(stdscr, maze):
    curses.curs_set(0)
    stdscr.clear()
    h = len(maze)
    w = len(maze[0])
    screen_h = h * 2 + 1
    screen_w = w * 2 + 1
    
    # build wall grid
    grid = [[0 for _ in range(screen_w)] for _ in range(screen_h)]
    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            gy = y * 2
            gx = x * 2
            if cell & TOP:
                grid[gy][gx] = 1
                grid[gy][gx + 1] = 1
                grid[gy][gx + 2] = 1
            if cell & BOTTOM:
                grid[gy + 2][gx] = 1
                grid[gy + 2][gx + 1] = 1
                grid[gy + 2][gx + 2] = 1
            if cell & LEFT:
                grid[gy][gx] = 1
                grid[gy + 1][gx] = 1
                grid[gy + 2][gx] = 1
            if cell & RIGHT:
                grid[gy][gx + 2] = 1
                grid[gy + 1][gx + 2] = 1
                grid[gy + 2][gx + 2] = 1
    for y in range(screen_h):
        for x in range(screen_w):
            if grid[y][x] == 0:
                stdscr.addch(y, x, " ")
                continue
            up = y > 0 and grid[y - 1][x]
            down = y < screen_h - 1 and grid[y + 1][x]
            left = x > 0 and grid[y][x - 1]
            right = x < screen_w - 1 and grid[y][x + 1]
            ch = wall_char(up, right, down, left)
            stdscr.addch(y, x, ch)
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    if len(sys.argv) != 2:
        print("Usage: python3 maze.py maze.txt")
        return
    maze = read_maze(sys.argv[1])
    draw_maze(stdscr, maze)


if __name__ == "__main__":
    curses.wrapper(main)