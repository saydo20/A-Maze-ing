import curses

def main(stdscr:object) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    art = [
        "  ██          ██   ██   ██   ██████ ██████        ██████  ██   ██  █████ ",
        " ████         ███ ███  ████      ██ ██              ██    ███  ██ ██     ",
        "██  ██        ███████ ██  ██    ██  █████           ██    ████ ██ ██  ██ ",
        "██████        ██ █ ██ ██████   ██   ██              ██    ██ ████ ██   ██" ,
        "██  ██        ██   ██ ██  ██  ██    ██              ██    ██  ███ ██  ██ " ,
        "██  ██ ██████ ██   ██ ██  ██ ██████ ██████ ██████ ██████  ██   ██  █████ "
    ]

    info_lines = [
        "By: Younes Mouafak, Saad Jdia",
        "1337 Coding School"
    ]

    menu_items = ["Start", "Quit"]
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        art_start_y = h // 6
        for i, line in enumerate(art):
            x = w // 2 - len(line) // 2
            y = art_start_y + i
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, line)
            stdscr.attroff(curses.color_pair(1))

        info_start_y = art_start_y + len(art) + 2
        for i, line in enumerate(info_lines):
            x = w // 2 - len(line) // 2
            y = info_start_y + i
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, line)
            stdscr.attroff(curses.color_pair(2))

        menu_start_y = info_start_y + len(info_lines) + 2
        for i, item in enumerate(menu_items):
            x = w // 2 - len(item) // 2
            y = menu_start_y + i
            if i == selected:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(3))
            else:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(4))

        help_text = "↑↓ Move | ENTER Select | Q Quit"
        x_help = w // 2 - len(help_text) // 2
        stdscr.addstr(h - 2, x_help, help_text)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP or key == curses.KEY_DOWN:
            selected = (selected + 1) % len(menu_items)

        elif key == 10:
            if menu_items[selected] == "Quit":
                exit(0)
            else:
                return

        elif key in (ord('q'), ord('Q')):
            break


curses.wrapper(main)
