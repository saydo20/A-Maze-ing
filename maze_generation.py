import random


class MazeGenerator:
    hexa = "0123456789ABCDEF"

    def __init__(self):
        self.north = 1
        self.east = 2
        self.south = 4
        self.west = 8

    @classmethod
    def apply_hole(cls, arr, col, row, width, height):
        cell = int(arr[row][col], 16)
        if row == 0:
            cell -= 1
        if row == height - 1:
            cell -= 4
        if col == 0:
            cell -= 8
        if col == width - 1:
            cell -= 2

        arr[row][col] = cls.hexa[cell]

    @classmethod
    def create_grid(cls, dict: dict):
        width = dict["WIDTH"]
        height = dict["HEIGHT"]
        x1, y1 = dict["ENTRY"]
        x2, y2 = dict["EXIT"]
        arr = []
        i = 0
        while i < height:
            row = []
            j = 0
            while j < width:
                row.append("F")
                j += 1
            arr.append(row)
            i += 1

        cls.apply_hole(arr, x1, y1, width, height)
        cls.apply_hole(arr, x2, y2, width, height)
        cls.create_visited_array(height, width)
        visited = cls.create_visited_array(height, width)
        cls.generate_maze(x1, y1, arr, visited, width, height)
        return arr

    @classmethod
    def remove_walls(cls, arr: list, row1, col1, row2, col2):
        cel1 = arr[row1][col1]
        cel2 = arr[row2][col2]
        cel1 = int(cel1, 16)
        cel2 = int(cel2, 16)
        if row2 == row1 - 1:
            cel1 -= 1
            cel2 -= 4
        elif row2 == row1 + 1:
            cel1 -= 4
            cel2 -= 1
        elif col2 == col1 - 1:
            cel1 -= 8
            cel2 -= 2
        elif col2 == col1 + 1:
            cel1 -= 2
            cel2 -= 8
        arr[row1][col1] = cls.hexa[cel1]
        arr[row2][col2] = cls.hexa[cel2]

    @classmethod
    def get_neighbors(cls, row, col, height, width):
        neibors = []
        if row - 1 >= 0:
            neibors.append([row - 1, col])
        if col + 1 < width:
            neibors.append([row, col + 1])
        if row + 1 < height:
            neibors.append([row + 1, col])
        if col - 1 >= 0:
            neibors.append([row, col - 1])
        return neibors

    @classmethod
    def create_visited_array(cls, height, width):
        arr = []
        j = 0
        while j < height:
            row = []
            i = 0
            while i < width:
                row.append(False)
                i += 1
            arr.append(row)
            j += 1
        return arr

    @classmethod
    def generate_maze(
        cls, current_row, current_col, grid, visited, width, height
    ):
        visited[current_row][current_col] = True
        neighbors = cls.get_neighbors(current_row, current_col, height, width)

        unvisited_neighbors = []
        for neighbor in neighbors:
            neighbor_row = neighbor[0]
            neighbor_col = neighbor[1]
            if visited[neighbor_row][neighbor_col] is False:
                unvisited_neighbors.append(neighbor)
        random.shuffle(unvisited_neighbors)
        for neighbor in unvisited_neighbors:
            neighbor_row = neighbor[0]
            neighbor_col = neighbor[1]
            if visited[neighbor_row][neighbor_col] is False:
                cls.remove_walls(grid, current_row, current_col,
                                 neighbor_row, neighbor_col)
                cls.generate_maze(neighbor_row, neighbor_col, grid,
                                  visited, width, height)
