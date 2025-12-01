import math
from utils import runner

class SafeCracker:

    def __init__(self, instructions, init_dial=50):
        self.instructions = instructions
        self.dial = init_dial

    def reset_dial(self, pos=50):
        self.dial = pos

    @runner
    def part_1(self):
        zero_count = 0
        for l in self.instructions:
            if l.startswith("L"):
                self.dial -= int(l[1:])
                self.dial %= 100
            elif l.startswith("R"):
                self.dial += int(l[1:])
                self.dial %= 100
            if self.dial == 0:
                zero_count += 1
        return zero_count

    @runner
    def part_2(self):
        total_zero_hits = 0
        for line in self.instructions:
            clicks = int(line[1:])
            # full rotations must go over 0
            total_zero_hits += clicks // 100
            remainder = clicks % 100
            if line.startswith("R"):
                if (self.dial + remainder) >= 100:  # if cross 0
                    total_zero_hits += 1
                self.dial = (self.dial + remainder) % 100
            elif line.startswith("L"):
                # self.dial must not be 0!
                if 0 < self.dial <= remainder:
                    total_zero_hits += 1
                self.dial = (self.dial - remainder) % 100
        return total_zero_hits

if __name__ == "__main__":
    with open('01.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    cracker = SafeCracker(lines)
    cracker.part_1()
    cracker.reset_dial()
    cracker.part_2()
