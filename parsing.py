"""
create a class Parser that has atributtes file and an empty dict
a method in the Parser class that pars the file and return the dict 
"""


class Parser:
    def __init__(self, file: str):
        self.file = file
        self.dict = {}

    def make_dic(self) -> dict:
        try:
            with open(self.file, "r") as f:
                a = f.read().split("\n")
            for i in a:
                i = i.split("=")
                if len(i) < 2 or len(i) > 2:
                    raise IndexError("the key has more than 1 value")
                key = i[0].strip()
                value = i[1].strip()
                self.dict[key] = value
            return self.dict
        except Exception as Error:
            print(f"caught an error : {Error}")


parser = Parser("config.txt")
print(parser.make_dic())
