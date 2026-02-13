def make_dic(file: str) -> dict:
    """Read a configuration file and parse it into a raw dictionary.

    Reads the file line by line, ignoring empty lines and comments.
    Each valid line must follow the 'KEY=VALUE' format. Duplicate
    keys are not allowed.

    Args:
        file (str): Path to the configuration file to read.

    Returns:
        dict: A dictionary mapping uppercase key strings to their
            raw string values as read from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IndexError: If a line does not contain exactly one '=' sign.
        ValueError: If a duplicate key is found in the file.
    """
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


def convert_dict(file: str) -> dict:
    """Parse and validate a configuration file into a typed dictionary.

    Calls make_dic to read the raw key-value pairs, then validates
    and converts each value to its appropriate Python type. Raises
    descriptive errors for any invalid or missing values.

    Expected keys and their types after conversion:
        - WIDTH (int): Must be a positive integer.
        - HEIGHT (int): Must be a positive integer.
        - ENTRY (list): Two non-negative integers [col, row] within
          the maze bounds.
        - EXIT (list): Two non-negative integers [col, row] within
          the maze bounds.
        - PERFECT (bool): Must be 'true' or 'false'.
        - OUTPUT_FILE (str): Must end with '.txt' and differ from
          the config file path.
        - SEED (str): Must not be empty. Use 'None' for a random seed.

    Args:
        file (str): Path to the configuration file to parse.

    Returns:
        dict: A fully validated dictionary with all values converted
            to their appropriate Python types.

    Raises:
        ValueError: If WIDTH or HEIGHT is negative.
        ValueError: If ENTRY or EXIT does not have exactly two coordinates.
        ValueError: If ENTRY or EXIT coordinates are negative or outside
            the maze bounds.
        ValueError: If ENTRY and EXIT are at the same position.
        ValueError: If PERFECT is not 'true' or 'false'.
        ValueError: If OUTPUT_FILE is empty, does not end with '.txt',
            or is the same as the config file.
        ValueError: If SEED is empty.
        NotImplementedError: If an unrecognized key is found in the file.
    """
 
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
                raise ValueError(
                    "the entry and the exit has to be in the maze")
            if dict[key][1] < 0:
                raise ValueError("the entry and the exit cannot be nugative")
            if dict[key][1] >= dict["HEIGHT"]:
                raise ValueError(
                    "the entry and the exit has to be in the maze")

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
        raise ValueError(
            "the entry and the exit cannot been in the same position")
    return dict
