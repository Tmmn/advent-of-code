from utils import runner

class Paver:

    def __init__(self, floor_plan):
        self.plan = [tuple(map(int, line.split(","))) for line in floor_plan]

    @runner
    def part_1(self):
        max_area = 0
        for i in range(len(self.plan)):
            for j in range(i + 1, len(self.plan)):
                x1, y1 = self.plan[i]
                x2, y2 = self.plan[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > max_area:
                    max_area = area
        return max_area

    @runner
    def part_2(self):
        pass

if __name__ == "__main__":
    with open('09.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    paver = Paver(lines)
    paver.part_1()
    paver.part_2()
