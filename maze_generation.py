import random
from collections import deque
from typing import Optional


class Cell:
    def __init__(self) -> None:
        self.value = "F"
        self.in_pattern = False


class MazeGenerator:
    hexa = "0123456789ABCDEF"
    @classmethod
    def create_grid(cls, dict: dict, height: int, width: int) -> list:
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
        return arr

    @classmethod
    def add_loops(cls, arr: list, height: int, width: int) -> None:
        total_cells = width * height
        walls_to_remove = total_cells // 15

        walls = []

        for row in range(height):
            for col in range(width):
                if arr[row][col].in_pattern:
                    continue
                if col < width - 1:
                    neighbor_col = col + 1
                    if not arr[row][neighbor_col].in_pattern:
                        cell_value = int(arr[row][col].value, 16)
                        if cell_value & 2:
                            walls.append((row, col, 'E'))
                if row < height - 1:
                    neighbor_row = row + 1
                    if not arr[neighbor_row][col].in_pattern:
                        cell_value = int(arr[row][col].value, 16)
                        if cell_value & 4:
                            walls.append((row, col, 'S'))
        if len(walls) > walls_to_remove:
            walls_selected = random.sample(walls, walls_to_remove)
        else:
            walls_selected = walls
        for (row, col, direction) in walls_selected:
            if direction == 'E':
                cls.remove_walls(arr, row, col, row, col + 1)
            elif direction == 'S':
                cls.remove_walls(arr, row, col, row + 1, col)

    @classmethod
    def pattern(cls, grid: list, height: int, width: int, entry_row: int, entry_col: int, exit_row: int, exit_col: int) -> None:
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
        if pattern_start_row < 0 or pattern_start_row + 6 > height:
            raise ValueError(f"Grid height ({height}) too small for pattern (needs at least 8)")
        if pattern_start_col < 0 or pattern_start_col + 8 > width:
            raise ValueError(f"Grid width ({width}) too small for pattern (needs at least 8)")
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
    def remove_walls(cls, arr: list, row1: int, col1: int, row2: int, col2: int) -> None:
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
    def get_neighbors(cls, row: int, col: int, height: int, width: int) -> list:
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
    def create_visited_array(cls, height: int, width: int) -> list:
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
        cls, entry_row: int, entry_col: int, grid: list, visited: list, width: int, height: int
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
            yield (current_row, current_col), (neighbor_row, neighbor_col)

    @classmethod
    def can_move(cls, grid: list, row1: int, col1: int, row2: int, col2: int) -> bool:
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
    def from_tuple_to_direction(cls, path: list) -> str:
        directions = ""
        i = 0
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            if c1 == c2 and r2 > r1:
                directions += "S"
            elif c1 == c2 and r2 < r1:
                directions += "N"
            elif r1 == r2 and c2 > c1:
                directions += "E"
            elif r1 == r2 and c2 < c1:
                directions += "W"
        return directions

    @classmethod
    def bfs_pathfind(cls, grid: list, entry: list, exit: list, width: int, height: int) -> list:
        entry_col, entry_row = entry
        exit_col, exit_row = exit
        queue: deque[tuple[int, int]] = deque()
        queue.append((entry_row, entry_col))
        visited = cls.create_visited_array(height, width)
        visited[entry_row][entry_col] = True
        parent: dict[tuple[int, int], Optional[tuple[int, int]]] = {}
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
            current: Optional[tuple[int, int]] = (exit_row, exit_col)
            while current is not None:
                path.append(current)
                current = parent.get(current)
            path.reverse()
            directions = cls.from_tuple_to_direction(path)
            return directions
        else:
            return None