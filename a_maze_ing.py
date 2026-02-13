import sys
import random
import curses
from typing import Any
from mazegen.Maze_drawing import Draw
from mazegen import parsing
from mazegen import maze_generation
from mazegen import banner


def prepare() -> tuple[list, dict, list]:
    """
    Parse arguments, build the initial grid, and apply the 42 pattern.

    Reads the configuration file path from command line arguments,
    parses it, creates the maze grid, applies the 42 pattern, and
    initializes the visited array

    Returns:
        tuple: A tuple containing:
            - arr (list): The 2D grid of maze cells with the
            42 pattern applied.
            - config (dict): The parsed configuration dictionary containing
              keys like WIDTH, HEIGHT, ENTRY, EXIT, SEED, PERFECT,
              OUTPUT_FILE.
            - visited (list): A 2D boolean array tracking visited cells
              during maze generation.

    Raises:
        ValueError: If the number of command line arguments is not exactly 2.
    """
    arg = sys.argv
    if len(arg) != 2:
        raise ValueError("The program must have exactly two arguments")
    config = parsing.convert_dict(arg[1])

    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry_col, entry_row = config["ENTRY"]
    exit_col, exit_row = config["EXIT"]

    seed = config["SEED"]
    if seed.lower() != "none":
        random.seed(seed)

    arr = maze_generation.MazeGenerator.create_grid(config, height, width)
    maze_generation.MazeGenerator.pattern(arr, height, width, entry_row,
                                          entry_col, exit_row, exit_col)

    visited = maze_generation.MazeGenerator.create_visited_array(height, width)
    return arr, config, visited


def finalize_and_save(arr: list, config: dict) -> str:
    """Finalize the maze after generation and save it to the output file.

    Optionally adds loops to make the maze imperfect based on the config,
    computes the shortest path from entry to exit using BFS, and writes
    the maze grid, entry, exit, and path to the output file.

    Args:
        arr (list): The 2D grid of fully generated maze cells.
        config (dict): The parsed configuration dictionary containing
            keys like WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, OUTPUT_FILE.

    Returns:
        str: The shortest path from entry to exit as a string of directions
            using 'N', 'E', 'S', 'W', or 'NO_PATH' if no path exists.
    """

    width = config["WIDTH"]
    height = config["HEIGHT"]

    if not config["PERFECT"]:
        maze_generation.MazeGenerator.add_loops(arr, height, width)

    path = maze_generation.MazeGenerator.bfs_pathfind(arr, config["ENTRY"],
                                                      config["EXIT"], width,
                                                      height)
    with open(config["OUTPUT_FILE"], "w") as f:
        for row in arr:
            for cell in row:
                f.write(str(cell.value))
            f.write("\n")
        f.write("\n")
        entry = tuple(config["ENTRY"])
        f.write(str(entry[0]))
        f.write(",")
        f.write(str(entry[1]))
        f.write("\n")
        exit = tuple(config["EXIT"])
        f.write(str(exit[0]))
        f.write(",")
        f.write(str(exit[1]))
        f.write("\n")
        f.write(path)
    return path


def animation(stdscr: Any, draw: Draw, arr: list, config: dict,
              visited: list) -> None:
    """Animate the DFS maze generation step by step in the terminal.

    Runs the DFS maze generator as a generator function, redrawing only
    the cells that change at each step to create a smooth animation effect.
    A short delay is applied between each step for visual clarity.

    Args:
        stdscr (curses.window): The main curses window used for rendering.
        draw (Draw): The Draw instance responsible for rendering maze cells.
        arr (list): The 2D grid of maze cells being generated.
        config (dict): The parsed configuration dictionary containing
            keys like WIDTH, HEIGHT, and ENTRY.
        visited (list): A 2D boolean array tracking visited cells
            during maze generation.

    Raises:
        SystemError: If the terminal screen is too small to display the maze.
    """

    height, width = stdscr.getmaxyx()
    height1 = config["HEIGHT"] * 3 + 7
    width1 = config["WIDTH"] * 4 + 1
    if height1 > height or width1 > width:
        raise SystemError("Screen too small ")
    height = config["HEIGHT"]
    width = config["WIDTH"]
    entry_col, entry_row = config["ENTRY"]

    for (r1, c1) in maze_generation.MazeGenerator.generate_maze(
        entry_row, entry_col, arr, visited, width, height
    ):
        draw.print_walls(int(arr[r1][c1].value, 16), r1, c1)
        stdscr.refresh()
        curses.napms(10)


if __name__ == "__main__":
    try:
        arr, config, visited = prepare()
        banner.run()
    except Exception as e:
        print(f"Unexpected error: {e} :( ")
        exit(0)
    except KeyboardInterrupt as e:
        print(f"See you Later {e}")
        exit(0)


def main(stdscr: Any, arr: list, config: dict, visited: list) -> None:
    """Run the main interactive maze application using curses.

    Initializes the curses display, runs the maze generation animation,
    finalizes and saves the maze, then enters an interactive loop
    responding to user keyboard input.

    Args:
        stdscr (curses.window): The main curses window provided by
            curses.wrapper.
        arr (list): The 2D grid of maze cells with the 42 pattern applied.
        config (dict): The parsed configuration dictionary containing
            keys like WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, OUTPUT_FILE.
        visited (list): A 2D boolean array tracking visited cells
            during maze generation.
    """

    stdscr.clear()
    curses.curs_set(0)

    draw = Draw(config, arr, stdscr)
    draw.print_grid()

    animation(stdscr, draw, arr, config, visited)

    draw.path = finalize_and_save(arr, config)

    draw.mark_entery_exit()
    draw.iterate()

    while True:
        draw.display_menu()
        char = stdscr.getkey()
        if char in ("q", "Q"):
            break
        if char in ("s", "S"):
            draw.show_path = not draw.show_path
            if draw.show_path:
                draw.print_path()
            else:
                draw.clear_path()
        if char in ("r", "R"):
            stdscr.clear()
            arr, config, visited = prepare()
            prev_color = draw.color
            draw = Draw(config, arr, stdscr)
            draw.color = prev_color
            draw.print_grid()

            animation(stdscr, draw, arr, config, visited)

            draw.path = finalize_and_save(arr, config)
            draw.mark_entery_exit()
            draw.iterate()
        if char in ("c", "C"):
            stdscr.clear()
            draw.display_menu()
            draw.allow_colors()
            draw.iterate()
        if char in ("p", "P"):
            stdscr.clear()
            draw.display_menu()
            draw.iterate()
            draw.play()
            stdscr.clear()
            draw.display_menu()
            draw.iterate()


try:
    curses.wrapper(main, arr, config, visited)
except KeyboardInterrupt as e:
    print(f"See you Later {e}")
    exit(0)
except Exception as e:
    print(f"Unexpected error: {e} :( ")
    exit(0)
