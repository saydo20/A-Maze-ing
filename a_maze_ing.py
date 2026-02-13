import sys
import random
import curses
from mazegen.Maze_drawing import Draw
from mazegen import parsing
from mazegen import maze_generation
from mazegen import banner

def prepare():
    """
    Phase 1: parse args + build initial grid + apply pattern.
    DO NOT generate the maze here (we want to animate that in curses).
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


def finalize_and_save(arr, config):
    """
    Phase 2: after generation is done (animated), optionally add loops,
    compute path, save output file.
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
        f.write(path if path else "NO_PATH")
    return path


def animation(stdscr, draw, arr, config, visited):
    """
    Runs the DFS generator and redraws only the changed cells per step.
    """
    height, width = stdscr.getmaxyx()
    height1 = config["HEIGHT"] * 3 + 8
    width1 = config["WIDTH"] * 4
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

def main(stdscr, arr, config, visited):
    stdscr.clear()
    curses.curs_set(0)

    # initial build (no maze generation yet)
    

    # draw empty frame/grid
    draw = Draw(config, arr, stdscr, path=None)
    draw.print_grid()

    animation(stdscr, draw, arr, config, visited)

    # after carving, compute path + save file
    draw.path = finalize_and_save(arr, config)

    # final touches
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
            draw = Draw(config, arr, stdscr, path=None)
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