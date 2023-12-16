import time
from pprint import pprint


def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(10e-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper


class CaveMirrors:
    def __init__(self, layout):
        self.layout = layout

    # PART 1
    @runner
    def part1(self):
        start_pos = (0, -1)
        start_dir = (0, 1)
        nr = self.nr_energized_tiles((start_pos, start_dir))
        return nr

    @runner
    def part2(self):
        # generate all possible start positions and directions, feed them one by one through part1
        # 2 * len(self.layout) + 2 * len(self.layout[0]
        y_comb = ([((-1, i), (1, 0)) for i in range(len(self.layout[0]))] +
                  [((len(self.layout), i), (-1, 0)) for i in range(len(self.layout[0]))])
        x_comb = ([((i, -1), (0, 1)) for i in range(len(self.layout))] +
                  [((i, len(self.layout[0])), (0, -1)) for i in range(len(self.layout))])
        all_combs = y_comb + x_comb
        energized = []
        for comb in all_combs:
            energized.append(self.nr_energized_tiles(comb))
        return max(energized)

    def nr_energized_tiles(self, start):
        """
        general: empty space ('.'), mirrors ('/' and '\'), and splitters ('|' and '-').
        beam starts at top left coming from left (y, x)
        create dict to store energized state and direction of beam to detect unnecessary movement

        walk through layout and when encountering splitters, create another beam (fill list of Beam objects)
        CHECK FOR DIRECTION
        """
        nr = 0
        beams = [Beam(start[0], start[1])]
        state = [[{"state": ".", "direction": (0, 0)}]*len(row) for row in self.layout]
        # do first move manually because it is starts outside of grid
        beams = self.do(".", beams[0], beams)

        while beams:
            remove_beams = []
            for i, beam in enumerate(beams):
                # change beam position
                beam.pos = self._new_direction(beam.pos, beam.direction)
                # check that beam is still in grid
                if not self.check_in_grid(beam):
                    remove_beams.append(i)
                    continue
                # change beam direction and create new beam if necessary
                beams = self.do(self.layout[beam.pos[0]][beam.pos[1]], beam, beams)
                # check if beam is following a path that is already being followed
                if (self.check_in_grid(beam) and state[beam.pos[0]][beam.pos[1]]["direction"] == beam.direction
                        and state[beam.pos[0]][beam.pos[1]]["state"] == "#"):
                    remove_beams.append(i)
                    continue
                # update state in state dict
                state[beam.pos[0]][beam.pos[1]] = {"state": "#", "direction": beam.direction}
            # remove not needed beams
            for i, beam_idx in enumerate(sorted(remove_beams)):
                del beams[beam_idx-i]

        # count energized tiles
        for row in state:
            for tile in row:
                if tile["state"] == "#":
                    nr += 1
        return nr

    def check_in_grid(self, beam):
        grid_y, grid_x = len(self.layout), len(self.layout[0])
        if 0 <= beam.pos[0] < grid_y and 0 <= beam.pos[1] < grid_x:
            return True
        return False

    def do(self, tile, beam, beams):
        ops = {".": self.do_point,                                    # empty space
               "/": self.do_mirror_left, "\\": self.do_mirror_right,  # mirrors
               "|": self.do_split_ver, "-": self.do_split_hor}        # splitters
        # execute
        beam.direction, beams = ops[tile](beam, beams)
        return beams

    # "."
    @staticmethod
    def do_point(beam, beams):
        return beam.direction, beams

    # "/"
    @staticmethod
    def do_mirror_left(beam, beams):
        if beam.direction in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            return (-1 * beam.direction[1], -1 * beam.direction[0]), beams
        return beam.direction, beams

    # "\"
    @staticmethod
    def do_mirror_right(beam, beams):
        if beam.direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            return (beam.direction[1], beam.direction[0]), beams
        return beam.direction, beams

    # "-"
    @staticmethod
    def do_split_hor(beam, beams):
        if beam.direction in [(1, 0), (-1, 0)]:
            beams.append(Beam(beam.pos, (0, 1)))
            return (0, -1), beams
        return beam.direction, beams

    # "|"
    @staticmethod
    def do_split_ver(beam, beams):
        if beam.direction in [(0, 1), (0, -1)]:
            beams.append(Beam(beam.pos, (-1, 0)))
            return (1, 0), beams
        return beam.direction, beams

    @staticmethod
    def _new_direction(pos, direct):
        return pos[0] + direct[0], pos[1] + direct[1]


class Beam:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction


if __name__ == "__main__":
    with open('16.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    lava_cave = CaveMirrors(lines)
    lava_cave.part1()
    lava_cave.part2()
