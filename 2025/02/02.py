import re
from utils import runner

class GiftShop:

    def __init__(self, ranges):
        self.ranges = [r.split("-") for r in ranges.split(",")]

    @runner
    def part_1(self):
        pattern = r"(\d+)\1"
        return self.evaluate_ranges(pattern)

    @runner
    def part_2(self):
        pattern = r"(\d+)\1+"
        return self.evaluate_ranges(pattern)

    def evaluate_ranges(self, pattern):
        total = 0
        for r in self.ranges:
            start = r[0]
            end = r[1]
            for n in range(int(start), int(end) + 1):
                if re.fullmatch(pattern, str(n)):
                    total += n
        return total

if __name__ == "__main__":
    with open('02.txt', 'r') as source:
        line = source.readline()[:-1]

    shop = GiftShop(line)
    shop.part_1()
    shop.part_2()
