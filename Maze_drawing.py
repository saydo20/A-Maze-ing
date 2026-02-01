import curses

class Draw:
    def __init__(self,height, width, file, screen):
            self.lines = []
            self.heigth = height
            self.width = width
            self.file = file
            self.screen = screen

    def print_grid(self):
        i = 0
        while(i < self.heigth):
            j = 0
            while(j < self.width):
                self.print_walls(int('F', 16), i, j)
                j += 1
            i += 1

    def iterate(self):
        with open(self.file, 'r') as file:
            height = 0
            while(height < self.heigth):
                str = file.readline()
                width = 0
                for char in str:
                    if(width < self.width):
                        self.print_walls(int(char, 16), height, width)
                        self.screen.refresh()
                        curses.napms(100)
                    width += 1
                height += 1

    def print_walls(self, cell_wals, height, width):
        
        x = height * 3
        y = width * 4

        if cell_wals & (1 << 0):
            self.screen.addstr(x, y," ━━━")
        else:
            self.screen.addstr(x, y,"    ")
        if cell_wals & (1 << 3):
            self.screen.addstr(x + 1, y,"┃")
            self.screen.addstr(x + 2, y,"┃")
        else :
            self.screen.addstr(x + 1, y," ")
            self.screen.addstr(x + 2, y," ")
        if height == self.heigth - 1:
            if cell_wals & (1 << 2):
                self.screen.addstr(x + 3, y," ━━━")
            else:
                self.screen.addstr(x, y,"    ")
        if width == self.width - 1:
            if cell_wals & (1 << 1):
                self.screen.addstr(x + 1, y + 4,"┃")
                self.screen.addstr(x + 2, y + 4,"┃")
            else :
                self.screen.addstr(x + 1, y," ")
                self.screen.addstr(x + 2, y," ")




def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    draw = Draw(5, 5, "maze.txt", stdscr)
    draw.print_grid()
    stdscr.refresh()
    curses.napms(100)
    draw.iterate()
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
