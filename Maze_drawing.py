import curses
import parsing
import sys
import maze_generation

try:
    arg = sys.argv
    if len(arg) != 2:
        raise ValueError("the prgram must has two argument")
    else:
        dict = parsing.convert_dict(arg[1])
        arr, path = maze_generation.MazeGenerator.create_grid(dict)
except Exception as Error:
    print(f"caught an error : {Error}")
    exit(1)



class Draw:
    def __init__(self,height, width, arr, screen):
            self.arr = []
            self.heigth = height
            self.width = width
            self.arr = arr
            self.screen = screen

    def print_grid(self):
        i = 0
        while(i < self.heigth):
            j = 0
            while(j < self.width):
                self.print_walls(int('F', 16), i, j)
                self.screen.refresh()
                # curses.napms(100)
                j += 1
            i += 1

    def iterate(self):
            height = 0
            for row in self.arr:
                width = 0
                for char in row:
                    self.print_walls(int(char.value, 16), height, width)
                    self.screen.refresh()
                    curses.napms(100)
                    width += 1
                height += 1

    def previous_cell(self, height, width, operation):
        if width < 0 or height < 0:
            return 1
        cell = int(self.arr[height][width].value, 16)
        if cell == 15:
            return 0
        return 1

    def print_walls(self, cell_wals, height, width):
        
        x = height * 3
        y = width * 4

        if cell_wals & (1 << 0):
            self.screen.addstr(x, y," ━━━")
        elif self.previous_cell(height - 1, width, "up"):
            self.screen.addstr(x, y,"    ")
        if cell_wals & (1 << 3):
            self.screen.addstr(x + 1, y,"┃")
            self.screen.addstr(x + 2, y,"┃")
        elif self.previous_cell(height, width - 1, "left"):
            self.screen.addstr(x + 1, y," ")
            self.screen.addstr(x + 2, y," ")
        if height == self.heigth - 1:
            if cell_wals & (1 << 2):
                self.screen.addstr(x + 3, y," ━━━")
        if width == self.width - 1:
            if cell_wals & (1 << 1):
                self.screen.addstr(x + 1, y + 4,"┃")
                self.screen.addstr(x + 2, y + 4,"┃")




def main(stdscr):
    stdscr.clear()
    # stdscr.curses(0)

    draw = Draw(dict["HEIGHT"], dict["WIDTH"], arr, stdscr)
    draw.print_grid()
    draw.iterate()
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
                
