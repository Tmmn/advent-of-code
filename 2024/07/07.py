import itertools

from utils import runner


class Calibrator:

    def __init__(self, calibrations):
        self.calibration = [[int(line.split(": ")[0]), [int(i) for i in line.split(": ")[1].split()]] for line in calibrations]

    @runner
    def part_1(self):
        correct = 0
        for line in self.calibration:
            correct += line[0] if self.check_line(line[1], line[0], ["*", "+"]) else 0
        return correct

    @runner
    def part_2(self):
        correct = 0
        for line in self.calibration:
            correct += line[0] if self.check_line(line[1], line[0], ["*", "+", "||"]) else 0
        return correct

    @staticmethod
    def check_line(line, target, operators):
        for comb in itertools.product(operators, repeat=len(line) - 1):
            result = line[0]
            for i, operation in enumerate(comb):
                if operation == "*":
                    result *= line[i + 1]
                elif operation == "+":
                    result += line[i + 1]
                elif operation == "||":
                    result = int("".join(map(str, [result, line[i + 1]])))
            if result == target:
                return True
        return False


if __name__ == "__main__":
    with open('07.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    calibrator = Calibrator(lines)
    calibrator.part_1()
    calibrator.part_2()
