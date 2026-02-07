import sys
import parsing
import maze_generation
import random

try:
    arg = sys.argv
    if len(arg) != 2:
        raise ValueError("The program must have exactly two arguments")
    dict = parsing.convert_dict(arg[1])
    width = dict["WIDTH"]
    height = dict["HEIGHT"]
    entry_col ,entry_row  = dict["ENTRY"]
    exit_col, exit_row = dict["EXIT"]
    seed = dict["SEED"]
    if seed.lower() != "none":
        random.seed(seed)
    perfect = dict["PERFECT"]
    arr = maze_generation.MazeGenerator.create_grid(height, width)
    maze_generation.MazeGenerator.pattern(arr, height, width, entry_row, entry_col, exit_row, exit_col)
    visited = maze_generation.MazeGenerator.create_visited_array(height, width)
    maze_generation.MazeGenerator.generate_maze(entry_row, entry_col, arr, visited, width, height)
    if not perfect:
        maze_generation.MazeGenerator.add_loops(arr, height, width)
    path = maze_generation.MazeGenerator.bfs_pathfind(arr, dict["ENTRY"], dict["EXIT"], width, height)
    with open(dict["OUTPUT_FILE"], "w") as f:
        for row in arr:
            for cell in row:
                f.write(str(cell.value))
            f.write("\n")
        f.write("\n")
        f.write(str(tuple(dict["ENTRY"])))
        f.write("\n")
        f.write(str(tuple(dict["EXIT"])))
        f.write("\n")
        if path:
            f.write(path)
        else:
            f.write("NO_PATH")
        import Maze_drawing
except ValueError as e:
    print(f"Validation error: {e}")
    exit(1)
except FileNotFoundError as e:
    print(f"File error: {e}")
    exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)