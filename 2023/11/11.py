import time


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


class SpaceImage:
    def __init__(self, image):
        self.img_original = image
        self.img_expanded, self.galaxies = self._expand_image()

    def _expand_image(self):
        new_image = self.img_original.copy()
        galaxies = []
        # remember which line is larger than it seems
        for y, row in enumerate(self.img_original):
            if "#" not in set(list(row)):
                new_image[y] = "¦"*len(new_image[0])
        # remember which row is larger than it seems
        # fill list of galaxy coordinates
        for x in range(len(new_image[0])):
            helper = set()
            for y in range(len(new_image)):
                helper.add(new_image[y][x])
                if new_image[y][x] == "#":
                    galaxies.append((y, x))
            if "#" not in helper:
                for y in range(len(new_image)):
                    new_image[y] = new_image[y][:x] + "¦" + new_image[y][x+1:]
        return new_image, sorted(galaxies)  # return expanded image of universe and sorted list of galxies

    @runner
    def find_shortest_paths(self, part=1):
        # make both parts work with the same function
        supported_parts = {1: 2, 2: 1000000}
        assert part in supported_parts, f"does not support calculating result for part {part}"
        # calculate paths for all galaxies * galaxies-1 / 2 combinations
        paths = []
        for index1 in range(len(self.galaxies)):
            for index2 in range(index1+1, len(self.galaxies)):
                paths.append(self._calc_shortest(self.galaxies[index1], self.galaxies[index2], supported_parts[part]))
        return f"{sum(paths)} for part {part}"

    def _calc_shortest(self, coord1, coord2, galaxy_is_bigger_by):
        # calculate distance between the two coordinates
        distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
        # apply galaxy_is_bigger_by for each line or row that appears smaller than it is
        for y in range(min(coord1[0], coord2[0]), max(coord1[0], coord2[0])+1):
            if self.img_expanded[y][coord1[1]] == "¦":
                distance += (galaxy_is_bigger_by - 1)
        for x in range(min(coord1[1], coord2[1]), max(coord1[1], coord2[1])+1):
            if self.img_expanded[coord1[0]][x] == "¦":
                distance += (galaxy_is_bigger_by - 1)
        return distance


if __name__ == "__main__":
    with open('11.txt', 'r') as source:
        space = [row[:-1] for row in source.readlines()]

    sky_over_metal_island = SpaceImage(space)
    sky_over_metal_island.find_shortest_paths(1)
    sky_over_metal_island.find_shortest_paths(2)
