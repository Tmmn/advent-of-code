from utils import runner

class Lab:

    def __init__(self, tachyon_diagram):
        self.tach = tachyon_diagram

    @runner
    def part_1(self):
        active_beams = set()
        active_beams.add(self.tach[0].index("S"))
        total_splits = 0
        for r in range(len(self.tach)):
            next_row_beams = set()
            for b in active_beams:
                if self.tach[r][b] == "^":
                    total_splits += 1
                    next_row_beams.update((b - 1, b + 1))
                else:
                    next_row_beams.add(b)
            active_beams = next_row_beams
        return total_splits

    @runner
    def part_2(self):
        memo = {}
        return self.count_timelines(0, self.tach[0].index("S"), memo)

    def count_timelines(self, y, x, memo):
        if y >= len(self.tach):
            return 1
        state = (y, x)
        if state in memo:
            return memo[state]
        if self.tach[y][x] == "^":
            result = self.count_timelines(y + 1, x - 1, memo) + self.count_timelines(y + 1, x + 1, memo)
        else:
            result = self.count_timelines(y + 1, x, memo)
        memo[state] = result
        return result

if __name__ == "__main__":
    with open('07.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    teleportation_lab = Lab(lines)
    teleportation_lab.part_1()
    teleportation_lab.part_2()
