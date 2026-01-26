"""
create functions:
the make dict function that create a dict that contain:
    all the keys,
    all the values
"""


def make_dic() -> dict:
    try:
        dict = {}
        with open("config.txt", "r") as f:
            a = f.read().split("\n")
        for i in a:
            i = i.split("=")
            if len(i) < 2 or len(i) > 2:
                raise IndexError("the key has more than 1 value")
            key = i[0].strip()
            value = i[1].strip()
            dict[key] = value
        return dict
    except Exception as Error:
        print(f"caught an error : {Error}")


"""
the second function that take that dict and check if it's valid or not
"""


def convert_dict():
    try:
        dict = make_dic()
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

            elif key == "PERFECT":
                if dict[key].lower() != "true":
                    if dict[key].lower() != "false":
                        raise ValueError('the PERFECT must be'
                                         ' "true" or "false"')

            elif key == "OUTPUT_FILE":
                pass
            else:
                raise (NotImplementedError("error : the file must"
                                           " contain only:"
                                           "\nWIDTH\nHEIGHT\nENTRY\nEXIT\n"
                                           "OUTPUT_FILE\nPERFECT"))

    except Exception as Error:
        print(f"Error : {Error}")
    print(dict)


convert_dict()
