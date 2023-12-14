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


class ReflectorDish:
    def __init__(self, platform):
        self.platform = platform

    @runner
    def load_north(self):
        # move all stones up
        new_platform = self._north(self.platform.copy())
        # now count all the stones
        return self._calc_load_north(new_platform)

    @staticmethod
    def _calc_load_north(platform):
        result = 0
        for y, row in enumerate(platform[::-1]):
            for place in row:
                if place == "O":
                    result += y+1
        return result

    @runner
    def spin(self):
        new_platform = self.platform.copy()
        cache = {}
        start_idx = None
        loop_after = None
        cycle_goal = 1_000_000_000  # NUMBER HAS TO BE CORRECT!!!
        for i in range(cycle_goal):
            new_platform = self._one_cycle(new_platform)
            if self._is_in_cache(cache, tuple(new_platform)):
                loop_after = i+1
                start_idx = list(filter(lambda x: cache[x] == tuple(new_platform), cache))[0]
                break
            cache[i+1] = tuple(new_platform)
        assert start_idx is not None and loop_after is not None, f"No loop detected"
        return self._calc_load_north(cache[((cycle_goal-start_idx) % (loop_after - start_idx))+start_idx])

    def _one_cycle(self, old_platform):
        cycle = [getattr(self, "_north"), getattr(self, "_west"), getattr(self, "_south"), getattr(self, "_east")]
        new_platform = old_platform.copy()
        for op in cycle:
            new_platform = op(new_platform)
        return new_platform

    @staticmethod
    def _is_in_cache(cache, new_platform):
        if new_platform in cache.values():
            return True
        return False

    def _north(self, platform):
        for y, row in enumerate(platform):
            for x, place in enumerate(row):
                if place == "O":
                    offset = -1
                    # move up
                    # could be improved to only move stone if new place for it is found
                    while platform[y+offset][x] == ".":
                        if y + offset < 0:
                            break
                        # move stone up one row
                        platform[y+offset] = self._replace_at_x(platform[y+offset], "O", x)
                        platform[y+offset+1] = self._replace_at_x(platform[y+offset+1], ".", x)
                        offset -= 1
        return platform

    def _west(self, platform):
        platform = self._rotate_right(platform)
        return self._rotate_left(self._north(platform))

    def _south(self, platform):
        return self._north(platform[::-1])[::-1]

    def _east(self, platform):
        platform = self._rotate_left(platform)
        return self._rotate_right(self._north(platform))

    @staticmethod
    def _replace_at_x(string, new, x):
        return string[:x] + new + string[x+1:]

    @staticmethod
    def _rotate_left(platform):
        return ["".join(row) for row in list(reversed(list(zip(*platform))))]

    @staticmethod
    def _rotate_right(platform):
        return ["".join(row) for row in list(zip(*reversed(platform)))]


if __name__ == "__main__":
    with open('14.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    lava_reflector_dish = ReflectorDish(lines)
    lava_reflector_dish.load_north()
    lava_reflector_dish.spin()
