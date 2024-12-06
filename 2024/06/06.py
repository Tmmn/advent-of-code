from copy import deepcopy
from utils import runner


class LeftGrid(Exception):
    pass

class Loop(Exception):
    pass

class Guard:

    def __init__(self, plan):
        self.plan = [[i for i in j] for j in plan]
        self.plan_backup = deepcopy(self.plan)
        self.pos = None
        self.orientation = None
        self.visited = None
        self.visited_from = None
        self.reset_guard()

    def reset_guard(self):
        self.pos = self.find_start()
        self.orientation = "U"
        self.visited = {self.pos}
        self.visited_from = {(self.pos[0], self.pos[1], self.orientation)}

    def find_start(self):
        for y, row in enumerate(self.plan):
            for x, val in enumerate(row):
                if val == "^":
                    return y, x

    def rotate(self):
        match self.orientation:
            case "U":
                self.orientation = "R"
            case "R":
                self.orientation = "D"
            case "D":
                self.orientation = "L"
            case "L":
                self.orientation = "U"

    def next_position(self):
        y, x = self.pos[0], self.pos[1]
        new_pos = (-1, -1)
        match self.orientation:
            case "U":
                new_pos = y - 1, x
            case "R":
                new_pos = y, x + 1
            case "D":
                new_pos = y + 1, x
            case "L":
                new_pos = y, x - 1
        if not self.check_bound(new_pos):
            raise LeftGrid
        return new_pos

    def check_bound(self, pos):
        y, x = pos
        if y < 0 or y >= len(self.plan) or x < 0 or x >= len(self.plan[0]):
            return False
        else:
            return True

    @runner
    def count_pos(self):
        self.predict_path()
        return len(self.visited)

    def predict_path(self):
        on_map = True
        while on_map:
            # move
            try:
                next_pos = self.next_position()
                while self.plan[next_pos[0]][next_pos[1]] == "#":
                    self.rotate()
                    next_pos = self.next_position()
            except LeftGrid:
                on_map = False
                break
            self.pos = next_pos[0], next_pos[1]
            # remember position
            self.visited.add(self.pos)
            pos_direct = (self.pos[0], self.pos[1], self.orientation)
            if pos_direct in self.visited_from:
                raise Loop
            else:
                self.visited_from.add(pos_direct)
        return len(self.visited)

    @runner
    def capture_guard(self):
        loops = 0
        to_check = self.visited.copy()
        for i, pos in enumerate(to_check):
            self.reset_guard()
            self.plan[pos[0]][pos[1]] = "#"
            try:
                self.predict_path()
            except Loop:
                loops += 1
            self.plan[pos[0]][pos[1]] = self.plan_backup[pos[0]][pos[1]]
        return loops


if __name__ == "__main__":
    with open('06.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    guard = Guard(lines)
    guard.count_pos()
    guard.capture_guard()
