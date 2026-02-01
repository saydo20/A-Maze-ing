import curses

class Draw:
    def __init__(self,height, width, file, screen):
            self.lines = []
            self.heigth = height
            self.width = width
            self.file = file
            self.screen = screen

    def iterate(self):
        with open(self.file, 'r') as file:
            height = 0
            while(height < self.heigth):
                str = file.readline()
                width = 0
                for char in str:
                    if(width < self.width):
                        self.print_walls(int(char, 16), height, width)
                    width += 1
                height += 1

    def print_walls(self, cell_wals, height, width):
        
        x = height * 3
        y = width * 4
        if cell_wals & (1 << 0):
            self.screen.addstr(x, y,"+━━━")
        if cell_wals & (1 << 3):
            self.screen.addstr(x + 1, y,"┃")
            self.screen.addstr(x + 2, y,"┃")
        if height == self.heigth - 1:
            if cell_wals & (1 << 2):
                self.screen.addstr(x + 3, y,"+━━━")
        if width == self.width - 1:
            if cell_wals & (1 << 1):
                self.screen.addstr(x + 1, y + 4,"┃")
                self.screen.addstr(x + 2, y + 4,"┃")




def main(stdscr):
    stdscr.clear()
    # stdscr.curses(0)

    draw = Draw(5, 5, "maze.txt", stdscr)
    draw.iterate()
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)