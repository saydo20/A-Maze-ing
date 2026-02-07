import curses
import parsing
import sys
import maze_generation
from a_maze_ing import arr
from a_maze_ing import path
from a_maze_ing import dict


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

    def print_grid(self):
        i = 0
        grid = [['F' for _ in range(self.width)] for _ in range(self.heigth)]
        for row in grid:
            j = 0
            for cell in row:
                self.print_walls(int(cell, 16), i, j)
                self.screen.refresh()
                j += 1
            i += 1

    def mark_entery_exit(self):
        height, width = self.infos["ENTRY"]
        x = height * 3
        y = width * 4
        self.screen.addstr(x + 2, y + 2, "S")
        height, width = self.infos["EXIT"]
        x = height * 3
        y = width * 4
        self.screen.addstr(x + 2, y + 2, "E")

    def color_cell(self, height, width, path):
        x = height * 3
        y = width * 4
        if path and self.show_path:
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
            color = curses.color_pair(1)
            self.screen.addstr(x + 1, y + 1, "███", color)
            self.screen.addstr(x + 2, y + 1, "███", color)
        elif self.show_path == False and path:
            self.screen.addstr(x + 1, y + 1, "   ")
            self.screen.addstr(x + 2, y + 1, "   ")
        else:
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
            color = curses.color_pair(2)
            self.screen.addstr(x + 1, y + 1, "███", color)
            self.screen.addstr(x + 2, y + 1, "███", color)

    def clear_path(self):
        x, y = self.infos["ENTRY"]
        x1, y1 = self.infos["EXIT"]
        path = self.path
        for char in path:
            if char == "S":
                x += 1
                self.screen.addstr(x * 3, y * 4 + 1,"   ")
            elif char == "N":
                x -= 1
                self.screen.addstr(x * 3 + 3, y * 4 + 1,"   ")
            elif char == "E":
                y += 1
                self.screen.addstr(x * 3 + 1, y * 4 ," ")
                self.screen.addstr(x * 3 + 2, y * 4 ," ")
            else:
                y -= 1
                self.screen.addstr(x * 3 + 1, y * 4 + 4 ," ")
                self.screen.addstr(x * 3 + 2, y * 4 + 4 ," ")
            if x == x1 and y == y1:
                break
            self.color_cell(x, y, 1)
            self.screen.refresh()
            curses.napms(50)

    def print_path(self):
        x, y = self.infos["ENTRY"]
        x1, y1 = self.infos["EXIT"]
        path = self.path
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        color = curses.color_pair(1)
        for char in path:

            if char == "S":
                x += 1
                self.screen.addstr(x * 3, y * 4 + 1,"███", color)
            elif char == "N":
                x -= 1
                self.screen.addstr(x * 3 + 3, y * 4 + 1,"███", color)
            elif char == "E":
                y += 1
                self.screen.addstr(x * 3 + 1, y * 4 ,"█", color)
                self.screen.addstr(x * 3 + 2, y * 4 ,"█", color)
            else:
                y -= 1
                self.screen.addstr(x * 3 + 1, y * 4 + 4 ,"█", color)
                self.screen.addstr(x * 3 + 2, y * 4 + 4 ,"█", color)
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
                    self.screen.refresh()
                    curses.napms(10)
                    width += 1
                height += 1
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
        if height >= 0 and width >= 0 and int(self.arr[height][width].value, 16) & (1 << 1):
            walls[3] = 1
        if height >= 0 and width >= 0 and int(self.arr[height][width].value, 16) & (1 << 2):
            walls[2] = 1
        width += 1
        if height >= 0 and int(self.arr[height][width].value, 16) & (1 << 3):
            walls[3] = 1
        if height >= 0 and int(self.arr[height][width].value, 16) & (1 << 2):
            walls[0] = 1

        if walls[0] and walls[1] and walls [2] and walls[3]:
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
        if which_border and (current & (1 << 3) or int(self.arr[height][width - 1].value, 16) & (1 << 1)):
            return 1
        elif which_border == 0 and (current & (1 << 0) or int(self.arr[height - 1][width].value, 16) & (1 << 2)):
            return 1
        return 0
  
    def print_corners(self, height, width):
        x = height * 3
        y = width * 4
        cell = self.check_walls(height, width)
        self.screen.addstr(x, y,cell)

        if width == self.width -1 :
            if height == 0:
                self.screen.addstr(x, y + 4,"╗")
            elif height <= self.heigth - 1:
                if self.borders_check(height, width, 0):
                    self.screen.addstr(x, y + 4,"╣")
                else:
                    self.screen.addstr(x, y + 4,"║")

        if height == self.heigth - 1:
            if width == 0:
                self.screen.addstr(x + 3, y,"╚")
            elif width == self.width -1:
                self.screen.addstr(x + 3, y + 4,"╝")
                if self.borders_check(height, width, 1):
                    self.screen.addstr(x + 3, y,"╩")
                else:
                    self.screen.addstr(x + 3, y,"═")
            elif self.borders_check(height, width, 1):
                self.screen.addstr(x + 3, y,"╩")
            else:
                self.screen.addstr(x + 3, y,"═")    

    def print_walls(self, cell_wals, height, width):
        
        x = height * 3
        y = width * 4
        
        self.print_corners(height, width)
        if cell_wals & (1 << 0):
            self.screen.addstr(x, y + 1,"═══")
        elif self.previous_cell(height - 1, width):
            self.screen.addstr(x, y + 1,"   ")
        if cell_wals & (1 << 3):
            self.screen.addstr(x + 1, y,"║")
            self.screen.addstr(x + 2, y,"║")
        elif self.previous_cell(height, width - 1):
            self.screen.addstr(x + 1, y," ")
            self.screen.addstr(x + 2, y," ")
        if height == self.heigth - 1:
            if cell_wals & (1 << 2):
                self.screen.addstr(x + 3, y + 1,"═══")
        if width == self.width - 1:
            if cell_wals & (1 << 1):
                self.screen.addstr(x + 1, y + 4,"║")
                self.screen.addstr(x + 2, y + 4,"║")




def main(stdscr):

        stdscr.clear()
        curses.curs_set(0)
        draw = Draw(dict, arr, stdscr, path)
        draw.print_grid()
        draw.iterate()
        while True:
            char = stdscr.getkey()
            if char == 'q' or char == 'Q':
                break
            if char == 's' or char == 'S':
                draw.show_path = not draw.show_path
                if draw.show_path:
                    draw.print_path()
                else:
                    draw.clear_path()
            if char == 'r' or char == 'R':
                pass



curses.wrapper(main)
                
