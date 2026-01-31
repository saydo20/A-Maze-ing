import sys
import parsing
import maze_generation

arg = sys.argv
if len(arg) != 2:
    raise ValueError("the prgram must has two argument")
else:
    dict = parsing.convert_dict(arg[1])
    arr, path = maze_generation.MazeGenerator.create_grid(dict)
    with open(dict["OUTPUT_FILE"], "w") as f:
        for row in arr:
            for cell in row:
                f.write(str(cell))
            f.write("\n")
        f.write("\n")
        f.write(str(tuple(dict["ENTRY"])))
        f.write("\n")
        f.write(str(tuple(dict["EXIT"])))
        f.write("\n")
        f.write(path)
