"""
create functions:
the make dict function that create a dict that contain:
    all the keys,
    all the values
"""


def make_dic(file: str) -> dict:
    try:
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

            key = parts[0].strip()
            value = parts[1].strip()
            config_dict[key] = value

        return config_dict

    except Exception as Error:
        print(f"Caught an error: {Error}")
        exit()


"""
the second function that take that dict and check if it's valid or not
"""


def convert_dict(file: str):
    try:
        dict = make_dic(file)
        for key in dict:
            if key == "WIDTH" or key == "HEIGHT":
                dict[key] = int(dict[key])
                if dict[key] < 0:
                    raise ValueError("\nthe value must no be negative\n")

            elif key == "ENTRY" or key == "EXIT":
                dict[key] = dict[key].split(',')

                if len(dict[key]) != 2:
                    raise ValueError(f"the {key} must has two coordinations")
                dict[key][0] = int(dict[key][0])
                dict[key][1] = int(dict[key][1])
                if dict[key][0] < 0:
                    raise ValueError("the entry cannot be nugative")
                if dict[key][0] > dict["WIDTH"] or dict[key][0] >= dict["HEIGHT"]:
                    raise ValueError("the entry has to be in the maze")
                if dict[key][1] < 0:
                    raise ValueError("the exit cannot be nugative")
                if dict[key][1] > dict["WIDTH"] or dict[key][1] >= dict["HEIGHT"]:
                    raise ValueError("the exit has to be in the maze")

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
                pass
            elif key == "SEED":
                pass
            else:
                raise (NotImplementedError("error : the file must"
                                           " contain only:"
                                           "\nWIDTH\nHEIGHT\nENTRY\nEXIT\n"
                                           "OUTPUT_FILE\nPERFECT"))
        return dict

    except Exception as Error:
        print(f"Error : {Error}")
        exit()
