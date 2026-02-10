import curses
import random


class Draw:
    def __init__(self, infos, arr, screen, path):
        self.arr = []
        self.heigth = infos["HEIGHT"]
        self.width = infos["WIDTH"]
        self.arr = arr
        self.screen = screen
        self.infos = infos
        self.path = path
        self.show_path = False
        self.color = curses.color_pair(0)

    def print_grid(self):
        i = 0
        for row in self.arr:
            j = 0
            for cell in row:
                self.print_walls(int(cell.value, 16), i, j)
                self.screen.refresh()
                j += 1
            i += 1

    def mark_entery_exit(self):
        entry_col, entry_row = self.infos["ENTRY"]
        x = entry_row * 3
        y = entry_col * 4
        self.screen.addstr(x + 2, y + 2, "S")
        exit_col, exit_row = self.infos["EXIT"]
        x = exit_row * 3
        y = exit_col * 4
        self.screen.addstr(x + 2, y + 2, "E")

    def color_cell(self, height, width, path):
        x = height * 3
        y = width * 4
        if path and self.show_path:
            curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
            color = curses.color_pair(6)
            self.screen.addstr(x + 1, y + 1, "███", color)
            self.screen.addstr(x + 2, y + 1, "███", color)
        elif self.show_path is False and path:
            self.screen.addstr(x + 1, y + 1, "   ")
            self.screen.addstr(x + 2, y + 1, "   ")
        else:
            curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_WHITE)
            color = curses.color_pair(7)
            self.screen.addstr(x + 1, y + 1, "███", color)
            self.screen.addstr(x + 2, y + 1, "███", color)

    def clear_path(self):
        col, row = self.infos["ENTRY"]
        col1, row1 = self.infos["EXIT"]
        path = self.path
        for char in path:
            if char == "S":
                row += 1
                self.screen.addstr(row * 3, col * 4 + 1, "   ")
            elif char == "N":
                row -= 1
                self.screen.addstr(row * 3 + 3, col * 4 + 1, "   ")
            elif char == "E":
                col += 1
                self.screen.addstr(row * 3 + 1, col * 4, " ")
                self.screen.addstr(row * 3 + 2, col * 4, " ")
            else:
                col -= 1
                self.screen.addstr(row * 3 + 1, col * 4 + 4, " ")
                self.screen.addstr(row * 3 + 2, col * 4 + 4, " ")
            if row == row1 and col == col1:
                break
            self.color_cell(row, col, 1)
            self.screen.refresh()
            curses.napms(50)

    def print_path(self):
        col, row = self.infos["ENTRY"]
        col1, row1 = self.infos["EXIT"]
        path = self.path
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
        color = curses.color_pair(6)
        for char in path:
            if char == "S":
                row += 1
                self.screen.addstr(row * 3, col * 4 + 1, "███", color)
            elif char == "N":
                row -= 1
                self.screen.addstr(row * 3 + 3, col * 4 + 1, "███", color)
            elif char == "E":
                col += 1
                self.screen.addstr(row * 3 + 1, col * 4, "█", color)
                self.screen.addstr(row * 3 + 2, col * 4, "█", color)
            else:
                col -= 1
                self.screen.addstr(row * 3 + 1, col * 4 + 4, "█", color)
                self.screen.addstr(row * 3 + 2, col * 4 + 4, "█", color)
            if row == row1 and col == col1:
                break
            self.color_cell(row, col, 1)
            self.screen.refresh()
            curses.napms(50)

    def iterate(self):
        height = 0
        for row in self.arr:
            width = 0
            for char in row:
                self.print_walls(int(char.value, 16), height, width)
                if char.in_pattern:
                    self.color_cell(height, width, 0)
                width += 1
            height += 1
            self.screen.refresh()
            curses.napms(10)
        self.mark_entery_exit()
        if self.show_path:
            self.show_path = not self.show_path

    def previous_cell(self, height, width):
        if width < 0 or height < 0:
            return 1
        cell = int(self.arr[height][width].value, 16)
        if cell == 15:
            return 0
        return 1

    def check_walls(self, height, width):
        walls = [0, 0, 0, 0]
        cell = int(self.arr[height][width].value, 16)
        if cell & (1 << 0):
            walls[0] = 1
        if cell & (1 << 3):
            walls[1] = 1
        width -= 1
        if (width >= 0 and int(self.arr[height][width].value, 16) & (1 << 0)):
            walls[2] = 1
        if (width >= 0 and int(self.arr[height][width].value, 16) & (1 << 1)):
            walls[1] = 1
        height -= 1
        if height >= 0 and width >= 0 and \
           int(self.arr[height][width].value, 16) & (1 << 1):
            walls[3] = 1
        if height >= 0 and width >= 0 and\
           int(self.arr[height][width].value, 16) & (1 << 2):
            walls[2] = 1
        width += 1
        if height >= 0 and int(self.arr[height][width].value, 16) & (1 << 3):
            walls[3] = 1
        if height >= 0 and int(self.arr[height][width].value, 16) & (1 << 2):
            walls[0] = 1

        if walls[0] and walls[1] and walls[2] and walls[3]:
            return "╬"
        if walls[0] and walls[1] and walls[3]:
            return "╠"
        if walls[1] and walls[2] and walls[3]:
            return "╣"
        if walls[0] and walls[1] and walls[2]:
            return "╦"
        if walls[3] and walls[0] and walls[2]:
            return "╩"
        if walls[0] and walls[1]:
            return "╔"
        if walls[1] and walls[2]:
            return "╗"
        if walls[0] and walls[3]:
            return "╚"
        if walls[2] and walls[3]:
            return "╝"
        if walls[0] or walls[2]:
            return "═"
        if walls[1] or walls[3]:
            return "║"
        else:
            return " "

    def borders_check(self, height, width, which_border):
        current = int(self.arr[height][width].value, 16)
        if which_border and (current & (1 << 3) or
           int(self.arr[height][width - 1].value, 16) & (1 << 1)):
            return 1
        elif which_border == 0 and \
            (current & (1 << 0) or
             int(self.arr[height - 1][width].value, 16) & (1 << 2)):
            return 1
        return 0

    def print_corners(self, height, width):
        x = height * 3
        y = width * 4
        cell = self.check_walls(height, width)
        self.screen.addstr(x, y, cell, self.color)

        if width == self.width - 1:
            if height == 0:
                self.screen.addstr(x, y + 4, "╗", self.color)
            elif height <= self.heigth - 1:
                if self.borders_check(height, width, 0):
                    self.screen.addstr(x, y + 4, "╣", self.color)
                else:
                    self.screen.addstr(x, y + 4, "║", self.color)

        if height == self.heigth - 1:
            if width == 0:
                self.screen.addstr(x + 3, y, "╚", self.color)
            elif width == self.width - 1:
                self.screen.addstr(x + 3, y + 4, "╝", self.color)
                if self.borders_check(height, width, 1):
                    self.screen.addstr(x + 3, y, "╩", self.color)
                else:
                    self.screen.addstr(x + 3, y, "═", self.color)
            elif self.borders_check(height, width, 1):
                self.screen.addstr(x + 3, y, "╩", self.color)
            else:
                self.screen.addstr(x + 3, y, "═", self.color)

    def print_walls(self, cell_wals, height, width):
        x = height * 3
        y = width * 4
        self.print_corners(height, width)
        if cell_wals & (1 << 0):
            self.screen.addstr(x, y + 1, "═══", self.color)
        elif self.previous_cell(height - 1, width):
            self.screen.addstr(x, y + 1, "   ", self.color)
        if cell_wals & (1 << 3):
            self.screen.addstr(x + 1, y, "║", self.color)
            self.screen.addstr(x + 2, y, "║", self.color)
        elif self.previous_cell(height, width - 1):
            self.screen.addstr(x + 1, y, " ", self.color)
            self.screen.addstr(x + 2, y, " ", self.color)
        if height == self.heigth - 1:
            if cell_wals & (1 << 2):
                self.screen.addstr(x + 3, y + 1, "═══", self.color)
        if width == self.width - 1:
            if cell_wals & (1 << 1):
                self.screen.addstr(x + 1, y + 4, "║", self.color)
                self.screen.addstr(x + 2, y + 4, "║", self.color)

    def display_menu(self):
        x = self.heigth * 3 + 2
        y = 0
        self.screen.addstr(x, y, "=== A-Maze-ing ===", curses.A_BOLD)
        self.screen.addstr(x + 1, y, "(S) - Show/Hide path", curses.A_BOLD)
        self.screen.addstr(x + 2, y, "(R) - Regenerate", curses.A_BOLD)
        self.screen.addstr(x + 3, y, "(C) - Change Colors", curses.A_BOLD)
        self.screen.addstr(x + 4, y, "(P) - Player mode", curses.A_BOLD)
        self.screen.addstr(x + 5, y, "(Q) - Quit", curses.A_BOLD)
        self.screen.addstr(x + 6, y, "Choice? :", curses.A_BOLD)
        self.screen.refresh()

    def allow_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        random_pair = random.choice(range(6))
        while self.color == curses.color_pair(random_pair):
            random_pair = random.choice(range(6))
        self.color = curses.color_pair(random_pair)
    def player_coins(self):
        col, row = self.infos["ENTRY"]
        col1, row1 = self.infos["EXIT"]
        path = self.path
        for char in path:
            if char == "S":
                row += 1
            elif char == "N":
                row -= 1
            elif char == "E":
                col += 1
            else:
                col -= 1
            if row == row1 and col == col1:
                break
            self.screen.addstr(row * 3 + 2, col * 4 + 2, "🌟")
            self.screen.refresh()
            curses.napms(10)

    def wall_checks(self, row, col, direction):
        cell = int(self.arr[row][col].value, 16)
        if direction == "up":
            if cell & (1 << 0) or \
            int(self.arr[row - 1][col].value, 16) & (1 << 2):
                return 0
        if direction == "down":
            if cell & (1 << 2) or \
            int(self.arr[row + 1][col].value, 16) & (1 << 0):
                return 0
        if direction == "left":
            if cell & (1 << 3) or \
            int(self.arr[row][col - 1].value, 16) & (1 << 1):
                return 0
        if direction == "right":
            if cell & (1 << 1) or \
            int(self.arr[row][col + 1].value, 16) & (1 << 3):
                return 0
        return 1

    def simulate(self):
        col, row = self.infos["ENTRY"]
        col1, row1 = self.infos["EXIT"]
        path = self.path
        for char in path:
            if char == "N":
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                row -= 1
            elif char == "S":
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                row += 1
            elif char == "W":
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                col -= 1
            elif char == "E":
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                col += 1
            if row == row1 and col == col1:
                break
            self.screen.addstr(row * 3 + 2, col * 4 + 2, "👾")
            self.screen.refresh()
            curses.napms(90)

    def play(self):
        self.screen.keypad(True)
        col, row = self.infos["ENTRY"]
        col1, row1 = self.infos["EXIT"]
        self.screen.addstr(row * 3 + 2, col * 4 + 2, "👾")
        self.player_coins()
        while True:
            key = self.screen.getkey()
            if key == "KEY_UP" and self.wall_checks(row, col, "up"):
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                row -= 1
            elif key == "KEY_DOWN" and self.wall_checks(row, col, "down"):
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                row += 1
            elif key == "KEY_LEFT" and self.wall_checks(row, col, "left"):
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                col -= 1
            elif key == "KEY_RIGHT" and self.wall_checks(row, col, "right"):
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                col += 1
            elif key in ("p", "P"):
                self.screen.addstr(row * 3 + 2, col * 4 + 2, "  ")
                self.simulate()
                break
            else:
                break
            if row == row1 and col == col1:
                break
            self.screen.addstr(row * 3 + 2, col * 4 + 2, "👾")
            self.screen.refresh()
            curses.napms(10)
