import sys
import parsing
import maze_generation

try:
    arg = sys.argv
    if len(arg) != 2:
        raise ValueError("The program must have exactly two arguments")
    dict = parsing.convert_dict(arg[1])
    arr, path = maze_generation.MazeGenerator.create_grid(dict)
    with open(dict["OUTPUT_FILE"], "w") as f:
        for row in arr:
            for cell in row:
                f.write(str(cell.value))
            f.write("\n")
        f.write("\n")
        f.write(str(dict["ENTRY"]))
        f.write("\n")
        f.write(str(dict["EXIT"]))
        f.write("\n")
        if path:
            f.write(path)
        else:
            f.write("NO_PATH")
except ValueError as e:
    print(f"Validation error: {e}")
    exit(1)
except FileNotFoundError as e:
    print(f"File error: {e}")
    exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)