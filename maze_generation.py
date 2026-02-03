import random
from collections import deque


class Cell:
    def __init__(self):
        self.value = "F"
        self.in_pattern = False


class MazeGenerator:
    hexa = "0123456789ABCDEF"

    def __init__(self):
        self.north = 1
        self.east = 2
        self.south = 4
        self.west = 8

    @classmethod
    def apply_hole(cls, arr, col, row, width, height):
        cell = int(arr[row][col].value, 16)
        if row == 0:
            cell -= 1
        elif row == height - 1:
            cell -= 4
        elif col == 0:
            cell -= 8
        elif col == width - 1:
            cell -= 2

        arr[row][col].value = cls.hexa[cell]

    @classmethod
    def create_grid(cls, dict: dict):
        width = dict["WIDTH"]
        height = dict["HEIGHT"]
        entry_col, entry_row = dict["ENTRY"]
        exit_col, exit_row = dict["EXIT"]
        # seed = dict["SEED"]
        # if seed is not None:
        #     random.seed(seed)
        perfect = dict["PERFECT"]
        arr = []
        i = 0
        while i < height:
            row = []
            j = 0
            while j < width:
                row.append(Cell())
                j += 1
            arr.append(row)
            i += 1
        cls.apply_hole(arr, entry_col, entry_row, width, height)
        cls.apply_hole(arr, exit_col, exit_row, width, height)
        cls.pattern(arr, height,
                    width, entry_col, entry_row, exit_col, exit_row)
        visited = cls.create_visited_array(height, width)
        cls.generate_maze(entry_row, entry_col, arr, visited, width, height)
        if not perfect:
            pass
        path = cls.bfs_pathfind(arr,
                                dict["ENTRY"], dict["EXIT"], width, height)
        return arr, path

    @classmethod
    def add_loops(cls, arr, height, width):
        total_cells = width * height
        walls_to_remove = total_cells // 10

        walls = []

        for row in range(height):
            for col in range(width):
                if arr[row][col].in_pattern:
                    continue
                if col < width - 1:
                    neighbor_col = col + 1
                    if not arr[row][neighbor_col].in_pattern:
                        cell_value = int(arr[row][col].value, 16)
                        if cell_value / 2 == 0:
                            walls.append((row, col, 'E'))
                if row < height - 1:
                    neighbor_row = row + 1
                    if not arr[row][neighbor_row].in_pattern:
                        cell_value = int(arr[row][col].value, 16)
                        if cell_value / 4 == 0:
                            walls.append((row, col, 'S'))
        if len(walls) > walls_to_remove:
            walls_selected = random.sample(walls, walls_to_remove)
        else:
            walls_selected = walls
        for (row, col, direction) in walls:
            if direction == 'E':
                cls.remove_walls(arr, row, col, row, col + 1)
            elif direction == 'S':
                cls.remove_walls(arr, row, col, row + 1, col)

    @classmethod
    def pattern(cls, grid, height, width, entry_col, entry_row, exit_col, exit_row):
        pattern_for = [
            (0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
            (3, 2), (4, 2)
        ]
        pattern_two = [
            (0, 4), (0, 5), (0, 6), (1, 6), (2, 6),
            (2, 5), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6)
        ]
        pattern_start_row = height // 2 - 2
        pattern_start_col = width // 2 - 3
        if pattern_start_row < 0 or pattern_start_row + 5 > height:
            raise ValueError(f"Grid height ({height}) too small for pattern (needs at least 7)")
        if pattern_start_col < 0 or pattern_start_col + 7 > width:
            raise ValueError(f"Grid width ({width}) too small for pattern (needs at least 7)")
        for row_offset, col_offset in pattern_for:
            actual_row = pattern_start_row + row_offset
            actual_col = pattern_start_col + col_offset
            if actual_row == exit_row and actual_col == exit_col:
                raise ValueError("Exit cannot be in the '42' pattern")
            if actual_row == entry_row and actual_col == entry_col:
                raise ValueError("Entry cannot be in the '42' pattern")
            grid[actual_row][actual_col].value = 'F'
            grid[actual_row][actual_col].in_pattern = True
        for row_offset, col_offset in pattern_two:
            actual_row = pattern_start_row + row_offset
            actual_col = pattern_start_col + col_offset
            if actual_row == exit_row and actual_col == exit_col:
                raise ValueError("Exit cannot be in the '42' pattern")
            if actual_row == entry_row and actual_col == entry_col:
                raise ValueError("Entry cannot be in the '42' pattern")
            grid[actual_row][actual_col].value = 'F'
            grid[actual_row][actual_col].in_pattern = True

    @classmethod
    def remove_walls(cls, arr: list, row1, col1, row2, col2):
        cel1 = arr[row1][col1].value
        cel2 = arr[row2][col2].value
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
        arr[row1][col1].value = cls.hexa[cel1]
        arr[row2][col2].value = cls.hexa[cel2]

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
        cls, entry_row, entry_col, grid, visited, width, height
    ):
        stack = []
        stack.append((entry_row, entry_col))
        visited[entry_row][entry_col] = True
        while stack:
            current_row, current_col = stack[-1]
            neighbors = cls.get_neighbors(
                current_row, current_col, height, width)
            unvisited_neighbors = []
            for neighbor in neighbors:
                neighbor_row = neighbor[0]
                neighbor_col = neighbor[1]
                if not visited[neighbor_row][neighbor_col]:
                    if not grid[neighbor_row][neighbor_col].in_pattern:
                        unvisited_neighbors.append(neighbor)
            if unvisited_neighbors:
                neighbor_row, neighbor_col = random.choice(unvisited_neighbors)
                cls.remove_walls(
                    grid, current_row, current_col, neighbor_row, neighbor_col)
                visited[neighbor_row][neighbor_col] = True
                stack.append((neighbor_row, neighbor_col))
            else:
                stack.pop()

    @classmethod
    def can_move(cls, grid, row1, col1, row2, col2):
        cell = int(grid[row1][col1].value, 16)
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