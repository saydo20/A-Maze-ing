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
        width, height = self.infos["ENTRY"]
        x = height * 3
        y = width * 4
        self.screen.addstr(x + 2, y + 2, "S")
        width, height = self.infos["EXIT"]
        x = height * 3
        y = width * 4
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
        y, x = self.infos["ENTRY"]
        y1, x1 = self.infos["EXIT"]
        path = self.path
        for char in path:
            if char == "S":
                x += 1
                self.screen.addstr(x * 3, y * 4 + 1, "   ")
            elif char == "N":
                x -= 1
                self.screen.addstr(x * 3 + 3, y * 4 + 1, "   ")
            elif char == "E":
                y += 1
                self.screen.addstr(x * 3 + 1, y * 4, " ")
                self.screen.addstr(x * 3 + 2, y * 4, " ")
            else:
                y -= 1
                self.screen.addstr(x * 3 + 1, y * 4 + 4, " ")
                self.screen.addstr(x * 3 + 2, y * 4 + 4, " ")
            if x == x1 and y == y1:
                break
            self.color_cell(x, y, 1)
            self.screen.refresh()
            curses.napms(50)

    def print_path(self):
        y, x = self.infos["ENTRY"]
        y1, x1 = self.infos["EXIT"]
        path = self.path
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
        color = curses.color_pair(6)
        for char in path:

            if char == "S":
                x += 1
                self.screen.addstr(x * 3, y * 4 + 1, "███", color)
            elif char == "N":
                x -= 1
                self.screen.addstr(x * 3 + 3, y * 4 + 1, "███", color)
            elif char == "E":
                y += 1
                self.screen.addstr(x * 3 + 1, y * 4, "█", color)
                self.screen.addstr(x * 3 + 2, y * 4, "█", color)
            else:
                y -= 1
                self.screen.addstr(x * 3 + 1, y * 4 + 4, "█", color)
                self.screen.addstr(x * 3 + 2, y * 4 + 4, "█", color)
            if x == x1 and y == y1:
                break
            self.color_cell(x, y, 1)
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
        self.screen.addstr(x + 4, y, "(Q) - Quit", curses.A_BOLD)
        self.screen.addstr(x + 5, y, "Choice? :", curses.A_BOLD)
        self.screen.refresh()

    def allow_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        random_pair = random.choice([0, 1, 2, 3, 4, 5])
        self.color = curses.color_pair(random_pair)
