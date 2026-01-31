import random
from collections import deque
# import sys

# sys.setrecursionlimit(5000) 


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
        elif row == height - 1:
            cell -= 4
        elif col == 0:
            cell -= 8
        elif col == width - 1:
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
        path = cls.bfs_pathfind(arr,
                                dict["ENTRY"], dict["EXIT"], width, height)
        return arr, path

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

    @classmethod
    def can_move(cls, grid, row1, col1, row2, col2):
        cell = int(grid[row1][col1], 16)
        if row2 == row1 - 1:
            return (cell & 1) == 0
        elif col2 == col1 + 1:
            return (cell & 2) == 0
        elif row2 == row1 + 1:
            return (cell & 4) == 0
        elif col2 == col1 - 1:
            return (cell & 8) == 0
        return False

    @classmethod
    def from_tuple_to_direction(cls, path):
        directions = ""
        i = 0
        for i in range(len(path) - 1):
            x, y = path[i]
            x2, y2 = path[i + 1]
            if y == y2 and x2 > x:
                directions += "S"
            elif y == y2 and x > x2:
                directions += "N"
            elif x == x2 and y2 > y:
                directions += "E"
            elif x == x2 and y > y2:
                directions += "W"
        return directions

    @classmethod
    def bfs_pathfind(cls, grid, entry, exit, width, height):
        entry_col, entry_row = entry
        exit_col, exit_row = exit
        queue = deque()
        queue.append((entry_row, entry_col))
        visited = cls.create_visited_array(height, width)
        visited[entry_row][entry_col] = True
        parent = {}
        parent[(entry_row, entry_col)] = None
        while queue:
            current_row, current_col = queue.popleft()
            if current_row == exit_row and current_col == exit_col:
                break
            neighbors = cls.get_neighbors(
                current_row, current_col, height, width)
            for neighbor in neighbors:
                neighbor_row = neighbor[0]
                neighbor_col = neighbor[1]
                if cls.can_move(grid, current_row, current_col,
                                neighbor_row, neighbor_col):
                    if not visited[neighbor_row][neighbor_col]:
                        visited[neighbor_row][neighbor_col] = True
                        parent[(neighbor_row, neighbor_col)] = (current_row,
                                                                current_col)
                        queue.append((neighbor_row, neighbor_col))
        if (exit_row, exit_col) in parent or (exit_row == entry_row and
                                              exit_col == entry_col):
            path = []
            current = (exit_row, exit_col)
            while current is not None:
                path.append(current)
                current = parent.get(current)
            path.reverse()
            path = cls.from_tuple_to_direction(path)
            return path
        else:
            return None
