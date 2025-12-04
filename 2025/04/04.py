from copy import deepcopy
from utils import runner

class Warehouse:

    def __init__(self, grid):
        self.grid = grid
        self._original_grid = deepcopy(grid)

    def reset_grid(self):
        self.grid = deepcopy(self._original_grid)

    @runner
    def part_1(self):
        return self.find_and_remove_rolls()

    @runner
    def part_2(self):
        last_removed = None
        total_removed = 0
        while last_removed != 0:
            last_removed = self.find_and_remove_rolls()
            total_removed += last_removed
        return total_removed

    def find_and_remove_rolls(self):
        num_removed = 0
        to_remove = []
        max_y = len(self.grid)
        max_x = len(self.grid[0])
        for y, i in enumerate(self.grid):
            for x, j in enumerate(i):
                if j == 1 and self.check_neighbors(x, y, max_x, max_y) < 4:
                    to_remove.append((y, x))
                    num_removed += 1
        for pos in to_remove:
            self.grid[pos[0]][pos[1]] = 2
        return num_removed

    def check_neighbors(self, x, y, max_x, max_y):
        neighbor_roll_count = 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                if not (a == 0 and b == 0) and 0 <= x + a < max_x and 0 <= y + b < max_y and self.grid[y + b][x + a] == 1:
                    neighbor_roll_count += 1
        return neighbor_roll_count

if __name__ == "__main__":
    with open('04.txt', 'r') as source:
        lines = [[1 if i == "@" else 0 for i in list(row[:-1])] for row in source.readlines()]
    house = Warehouse(lines)
    house.part_1()
    house.reset_grid()
    house.part_2()
