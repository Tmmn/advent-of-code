import time


def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(1e-6 * execution_time):.3f} ms to execute: {result}")
        return result
    return wrapper


class Trench:
    def __init__(self, build_plan):
        # PART 1: [0] direction, [1] amount of digging in direction, [2] color
        # PART 2: [2] 5 digits amount, last digit direction, [:2] color
        self.build_plan = [[step.split()[0]] + [int(step.split()[1])] + [step.split()[2].strip("()")]
                           for step in build_plan]
        self.directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
        # 0 means R, 1 means D, 2 means L, and 3 means U.
        self.hex_directions = {"0": (1, 0), "1": (0, 1), "2": (-1, 0), "3": (0, -1)}

    @runner
    def lava_capacity(self, part=1):
        supported_parts = [1, 2]
        assert part in supported_parts, f"do not support solution for part {part}"
        if part == 1:
            trenches = self.get_outline()
            lake = self.fill_hole(trenches)
            return f"Part 1 = {len(lake)}"
        else:
            trench_corners, boundary_points = self.get_outline_hexadecimal()
            interior_points = self.shoelace(trench_corners)
            # https://en.wikipedia.org/wiki/Pick%27s_theorem
            total_points = interior_points + (boundary_points // 2) + 1
            return f"Part 2 = {total_points}"

    def shoelace(self, trench_corners):
        # https://en.wikipedia.org/wiki/Shoelace_formula
        area = 0
        for i in range(len(trench_corners)-1):
            (x1, y1), (x2, y2) = trench_corners[i:i + 2]
            area += x1*y2 - x2*y1
        return abs(area) // 2

    def fill_hole(self, trenches):
        top_left = min(trenches)
        bottom_right = max(trenches)

        q = [self.new_position(top_left, (1, 1))]
        while q:
            pos = q.pop()
            for direction in self.directions.values():
                new_pos = self.new_position(pos, direction)
                if new_pos not in trenches:
                    q.append(new_pos)
                    trenches.add(new_pos)
        return trenches

    def get_outline(self):
        # PART 1
        position = (0, 0)
        trench_map = {position}
        for step in self.build_plan:
            for _ in range(step[1]):
                position = self.new_position(position, self.directions[step[0]])
                trench_map.add(position)
        return trench_map

    def get_outline_hexadecimal(self):
        # PART 2
        position = (0, 0)
        trench_corners = [position]
        boundary = 0
        for step in self.build_plan:
            nr_steps = int(step[2][1:6], base=16)
            boundary += nr_steps
            direction = self.hex_directions[step[2][6]]
            position = self.new_position(position, (direction[0]*nr_steps, direction[1]*nr_steps))
            trench_corners.append(position)
        return trench_corners, boundary

    @staticmethod
    def new_position(pos, direction):
        return pos[0] + direction[0], pos[1] + direction[1]


if __name__ == "__main__":
    with open('18.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    lava_trench = Trench(lines)
    lava_trench.lava_capacity(1)
    lava_trench.lava_capacity(2)
