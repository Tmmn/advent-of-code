import time

'''
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, 
      but your sketch doesn't show what shape the pipe has.
'''


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


class PipeSystem:
    def __init__(self, system):
        # helper dictionaries to translate directions to x, y operations and pipe map symbols to directions
        self.directions = {  # (y, x)
            "north": (-1, 0),
            "south": (1, 0),
            "west": (0, -1),
            "east": (0, 1)
        }
        self.pipe_translations = {
            "|": (self.directions["north"], self.directions["south"]),
            "-": (self.directions["east"], self.directions["west"]),
            "L": (self.directions["north"], self.directions["east"]),
            "J": (self.directions["north"], self.directions["west"]),
            "7": (self.directions["south"], self.directions["west"]),
            "F": (self.directions["south"], self.directions["east"]),
            ".": ((0, 0), (0, 0))
        }
        # store given pipe system
        self.pipe_system = system
        # get starting coordinates of point S
        self.start_point = None
        for y, row in enumerate(self.pipe_system):
            for x, tile in enumerate(row):
                if tile == "S":
                    self.start_point = (y, x)
        assert self.start_point is not None, "No start point found in pipe_system"
        # replace S in pipe system by the correct pipe symbol
        # needed to ensure implementation for Part 2 works with all inputs
        # (could be improved to only calculate starting directions once)
        start_dirs = []
        for direction in self.directions:
            next_tile_from_start = self._add_tuple(self.start_point, self.directions[direction])
            for operation in self.pipe_translations[self.pipe_system[next_tile_from_start[0]][next_tile_from_start[1]]]:
                connecting_tile = self._add_tuple(next_tile_from_start, operation)
                if connecting_tile == self.start_point:
                    start_dirs.append(direction)
        replace_by = list(filter(
            lambda p: self.pipe_translations[p] == (self.directions[start_dirs[0]], self.directions[start_dirs[1]])
                      or self.pipe_translations[p] == (self.directions[start_dirs[1]], self.directions[start_dirs[0]]),
            self.pipe_translations))[0]
        self.pipe_system[self.start_point[0]] = (
                self.pipe_system[self.start_point[0]][:self.start_point[1]] + replace_by
                + self.pipe_system[self.start_point[0]][self.start_point[1] + 1:])

    @runner
    def longest_distance(self):
        # look around starting point and take the first best direction that is in the loop
        next_position, not_this_direction = self._find_starting_direction()
        # initiate steps to 1
        steps = 1
        while next_position != self.start_point:
            # calculate next tile position
            # remember where we came from that we traverse the loop only in one direction
            next_position, not_this_direction = self._next_tile(next_position, not_this_direction)
            steps += 1
        return int(steps / 2)

    @runner
    def enclosed_loop(self):
        # initiate 2d array with 0s and go forwards in loop until back at start. fill all positions of loop with 1
        helper_array = [[0 for _ in row] for row in self.pipe_system]
        next_position, not_this_direction = self._find_starting_direction()
        helper_array[next_position[0]][next_position[1]] = 1
        while next_position != self.start_point:
            next_position, not_this_direction = self._next_tile(next_position, not_this_direction)
            helper_array[next_position[0]][next_position[1]] = 1

        # fill inside of loop in helper_array and count how many tiles are inside
        # count crossing if connection upwards exist and if crossing is an odd number, we know we are inside the loop
        inside_tiles = 0
        for y, row in enumerate(helper_array):
            crossings = 0
            for x, tile in enumerate(row):
                if (tile == 1 and (self.pipe_system[y][x] == "J"
                                   or self.pipe_system[y][x] == "L"
                                   or self.pipe_system[y][x] == "|")):
                    crossings += 1
                elif tile == 0 and crossings % 2 == 1:
                    inside_tiles += 1
                    helper_array[y][x] = 8
        return inside_tiles

    def _find_starting_direction(self):
        # go into all four possible directions
        for direction in self.directions:
            # calculate the coords of the tile in one direction
            next_tile_from_start = self._add_tuple(self.start_point, self.directions[direction])
            # see if the tile leads back to the start node
            for operation in self.pipe_translations[self.pipe_system[next_tile_from_start[0]][next_tile_from_start[1]]]:
                connecting_tile = self._add_tuple(next_tile_from_start, operation)
                # if it leads back to start node,
                # return coords of next tile and coords of start tile (do not go back there)
                if connecting_tile == self.start_point:
                    return next_tile_from_start, self.start_point
        raise Exception(f"No starting direction found for start point {self.start_point}")

    def _next_tile(self, position, not_back_to_here):
        # do all operation or position
        for operation in self.pipe_translations[self.pipe_system[position[0]][position[1]]]:
            next_position = self._add_tuple(position, operation)
            # if the next position does not lead back where we came from
            if next_position != not_back_to_here:
                return next_position, position
        raise Exception(f"could not find next tile from {position} that does not lead back to {not_back_to_here}")

    @staticmethod
    def _add_tuple(tuple1, tuple2):
        x1, y1 = tuple1
        x2, y2 = tuple2
        return x1 + x2, y1 + y2


if __name__ == "__main__":
    with open('10.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    metal_pipes = PipeSystem(lines)
    metal_pipes.longest_distance()
    metal_pipes.enclosed_loop()
