import time
import math


# decorator that prints result that execution time when calling calculate_winnings method
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


class DesertMap:
    def __init__(self, instructions, network):
        self.instructions = instructions
        self.network = {point.split(" = ")[0]: tuple(point.split(" = ")[1].strip("()").split(", ")) for point in network}

    @runner
    def steps_required(self):
        steps = 0
        point_pointer = "AAA"
        instruction_pointer = 0
        while point_pointer != "ZZZ":
            match self.instructions[instruction_pointer]:
                case "L":
                    point_pointer = self.network[point_pointer][0]
                case "R":
                    point_pointer = self.network[point_pointer][1]
            steps += 1
            instruction_pointer = (instruction_pointer + 1) % len(self.instructions)
        return steps

    @runner
    def simultaneous_steps_required(self):
        steps_to_ends = []
        starting_points = [start for start in self.network.keys() if start.endswith("A")]
        for starting_point in starting_points:
            steps = 0
            point_pointer = starting_point
            instruction_pointer = 0
            while not point_pointer.endswith("Z"):
                match self.instructions[instruction_pointer]:
                    case "L":
                        point_pointer = self.network[point_pointer][0]
                    case "R":
                        point_pointer = self.network[point_pointer][1]
                instruction_pointer = (instruction_pointer + 1) % len(self.instructions)
                steps += 1
            steps_to_ends.append(steps)
        return math.lcm(*steps_to_ends)


if __name__ == "__main__":
    with open('08.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    haunted_desert = DesertMap(lines[0], lines[2:])
    haunted_desert.steps_required()
    haunted_desert.simultaneous_steps_required()
