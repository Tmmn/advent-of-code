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


class MirrorReflections:
    def __init__(self, image_blocks):
        # used for vertical analysis
        self.blocks = image_blocks

    @runner
    def note_summary(self, part=1):
        supported_parts = [1, 2]
        assert part in supported_parts, f"do not support solution for part {part}"

        solution = 0
        for block in self.blocks:
            solution += self._vertical_and_horizontal(block, 0 if part == 1 else 1)

        return f"Solution for part {part}: {solution}"

    def _vertical_and_horizontal(self, block, hamming_distance):
        # vertical
        result = self._get_line(block, hamming_distance)
        if result is not False:
            return result

        # rotate block
        block_rotated = []
        for i in range(len(block[0])):
            string = ""
            for j in range(0, len(block)):
                string += block[j][i]
            block_rotated.append(string)
        # horizontal
        result = self._get_line(block_rotated, hamming_distance)
        if result is not False:
            return 100 * result
        raise Exception(f"Could not find solution for block {block}")

    @staticmethod
    def _get_line(block, hamming_distance):
        for i in range(1, len(block[0])):
            # from left to i and i to right
            # make them equal length
            # check if reversed right is equal left
            equal = 0
            hamming_lines = 0
            for row in block:
                left = row[:i]
                right = row[i:]
                if len(left) > len(right):
                    left = left[len(left)-len(right):]
                elif len(right) > len(left):
                    right = right[:len(left)]
                if left == right[::-1]:
                    equal += 1
                elif left != right[::-1] and sum(left[i] != right[::-1][i] for i in range(len(left))) == hamming_distance:
                    hamming_lines += 1
            if equal == len(block)-hamming_distance and (hamming_lines == 1 if hamming_distance > 0 else True):
                return i
        return False


if __name__ == "__main__":
    with open('13.txt', 'r') as source:
        lines = source.read().split("\n\n")
        lines = [bl.splitlines() for bl in lines]
    lava_valley = MirrorReflections(lines)
    lava_valley.note_summary(1)
    lava_valley.note_summary(2)
