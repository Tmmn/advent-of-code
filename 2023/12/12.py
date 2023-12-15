"""
ONLY SOLVED PART 1!
"""
import time


def runner(func):
    def wrapper(*args):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {execution_time:.3f} s to execute "
              f"and the result is: {result}")
        return result
    return wrapper


class HotSprings:
    def __init__(self, spring_data):
        self.spring_data = spring_data

    @runner
    def repair_combinations(self):
        valid_combinations = 0
        for row in self.spring_data:
            spring, grouping = row.split()
            grouping = [int(i) for i in grouping.split(",")]
            nr_of_qmarks = spring.count('?')
            combinations = self._get_combinations(nr_of_qmarks)
            for combination in combinations:
                combination = list(combination)
                potential_spring = "".join([char if char != "?" else combination.pop(0) for char in spring])
                if self._is_valid_combination(potential_spring, grouping):
                    valid_combinations += 1
        return valid_combinations

    @staticmethod
    def _is_valid_combination(combination, grouping):
        groups = [g for g in combination.split(".") if g]
        if len(groups) != len(grouping):
            return False
        for actual_group, expected_group in zip(groups, grouping):
            if len(actual_group) != expected_group:
                return False
        return True

    @staticmethod
    def _get_combinations(repeats):
        # works like product from itertools
        symbols = ["#", "."]
        pools = [tuple(symbols)] * repeats
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        return [tuple(prod) for prod in result]
        # return result


if __name__ == "__main__":
    with open('12.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    hot_springs_on_gear_island = HotSprings(lines)
    hot_springs_on_gear_island.repair_combinations()
