"""
create functions:
the make dict function that create a dict that contain:
    all the keys,
    all the values
"""


def make_dic(file: str) -> dict:
    config_dict = {}
    with open(file, "r") as f:
        lines = f.read().split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split("=")
        if len(parts) != 2:
            raise IndexError(f"Line '{line}' must have exactly one '='")

        key = parts[0].strip().upper()
        value = parts[1].strip()
        if key in config_dict:
            raise ValueError(f"Duplicate key '{key}' found at line {line}")
        config_dict[key] = value
    return config_dict


"""
the second function that take that dict and check if it's valid or not
"""


def convert_dict(file: str) -> dict:
    dict = make_dic(file)
    for key in dict:
        if key == "WIDTH" or key == "HEIGHT":
            dict[key] = int(dict[key])
            if dict[key] < 0:
                raise ValueError("\nthe value must be positive\n")

        elif key == "ENTRY" or key == "EXIT":
            dict[key] = dict[key].split(',')

            if len(dict[key]) != 2:
                raise ValueError(f"the {key} must has two coordinations")
            dict[key][0] = int(dict[key][0])
            dict[key][1] = int(dict[key][1])
            if dict[key][0] < 0:
                raise ValueError("the entry and the exit cannot be nugative")
            if dict[key][0] >= dict["WIDTH"]:
                raise ValueError("the entry and the exit has to be in the maze")
            if dict[key][1] < 0:
                raise ValueError("the entry and the exit cannot be nugative")
            if dict[key][1] >= dict["HEIGHT"]:
                raise ValueError("the entry and the exit has to be in the maze")

        elif key == "PERFECT":
            if dict[key].lower() != "true":
                if dict[key].lower() != "false":
                    raise ValueError('the PERFECT must be'
                                        ' "true" or "false"')
            if dict[key].lower() == "true":
                dict[key] = True
            else:
                dict[key] = False
        elif key == "OUTPUT_FILE":
            if dict[key] == file:
                raise ValueError("the OUTPUT_FILE can't be the config.txt")
            if not dict[key]:
                raise ValueError("OUTPUT_FILE cannot be empty")
            if not dict[key].endswith(".txt"):
                raise ValueError("OUTPUT_FILE must end with .txt")

        elif key == "SEED":
            if not dict[key]:
                raise ValueError("the SEED cannot be empty")
        else:
            raise (NotImplementedError("the file must"
                                        " contain only:"
                                        "\nWIDTH\nHEIGHT\nENTRY\nEXIT\n"
                                        "OUTPUT_FILE\nPERFEC\nSEED"))
    if dict["ENTRY"] == dict["EXIT"]:
                raise ValueError("the entry and the exit cannot been in the same position")
    return dict