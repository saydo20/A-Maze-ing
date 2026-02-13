import curses
from typing import Any


def main(stdscr: Any) -> None:
    """Display the animated banner and interactive main menu.

    Renders the A-Maze-ing ASCII art banner, author information, and
    a navigable menu using curses. The user can select to start the
    program or quit using keyboard arrow keys and Enter.

    Args:
        stdscr (Any): The main curses window provided by curses.wrapper.
    """
    curses.curs_set(0)
    stdscr.keypad(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    art = [
        "  ██          ██   ██   ██   ██████ ██████"
        "        ██████  ██   ██  █████ ",
        " ████         ███ ███  ████      ██ ██    "
        "          ██    ███  ██ ██     ",
        "██  ██        ███████ ██  ██    ██  █████ "
        "          ██    ████ ██ ██  ██ ",
        "██████        ██ █ ██ ██████   ██   ██    "
        "          ██    ██ ████ ██   ██",
        "██  ██        ██   ██ ██  ██  ██    ██    "
        "          ██    ██  ███ ██  ██ ",
        "██  ██ ██████ ██   ██ ██  ██ ██████ ██████"
        " ██████ ██████  ██   ██  █████ "
    ]

    info_lines = [
        "By: Younes Mouafak, Saad Jdia",
        "1337 Coding School"
    ]

    menu_items = ["Start", "Quit"]
    selected = 0

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    art_start_y = h // 6
    i = 0
    for line in art:
        x = w // 2 - len(line) // 2
        y = art_start_y + i
        stdscr.addstr(y, x, line, curses.color_pair(1))
        i += 1

    info_start_y = art_start_y + 6 + 2
    i = 0
    for line in info_lines:
        x = w // 2 - len(line) // 2
        y = info_start_y + i
        stdscr.addstr(y, x, line, curses.color_pair(2))
        i += 1

    help_text = "↑↓ Move | ENTER Select | Q Quit"
    x_help = w // 2 - len(help_text) // 2
    stdscr.addstr(h - 2, x_help, help_text)

    while True:

        menu_start_y = info_start_y + 4
        i = 0
        for item in menu_items:
            x = w // 2 - len(item) // 2
            y = menu_start_y + i
            if i == selected:
                stdscr.addstr(y, x, item, curses.color_pair(3))
            else:
                stdscr.addstr(y, x, item)
            i += 1

        stdscr.refresh()
        key = stdscr.getkey()

        if key == "KEY_UP" or key == "KEY_DOWN":
            selected = 1 - selected

        elif key == "\n":
            if menu_items[selected] == "Quit":
                exit(0)
            else:
                return

        elif key in ('q', 'Q'):
            exit(0)


def run() -> None:
    """Launch the banner and main menu using curses.

    Wraps the main function with curses.wrapper to initialize the
    curses environment, handle cleanup automatically, and restore
    the terminal to its original state on exit.
    """
    curses.wrapper(main)
