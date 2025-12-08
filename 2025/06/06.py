from math import prod
from utils import runner

class Crusher:

    def __init__(self, math):
        self.math = [line.split() for line in math]
        self.math2 = [list(line) for line in math]

    @runner
    def part_1(self):
        instructions = self.math[-1]
        answer = 0
        for i in range(len(self.math[0])):
            answer += self.calc([int(line[i]) for line in self.math[:-1]], instructions[i])
        return answer

    @runner
    def part_2(self):
        instructions = self.math[-1]
        num_count = len(instructions) - 1
        answer = 0
        numbers = []
        for i in range(len(self.math2[0]) - 1, -1, -1):
            if all([line[i] == " " for line in self.math2[:-1]]):
                answer += self.calc(numbers, instructions[num_count])
                num_count -= 1
                numbers = []
            else:
                numbers.append(int("".join(line[i] for line in self.math2[:-1])))
        answer += self.calc(numbers, instructions[num_count])
        return answer

    @staticmethod
    def calc(line, instr):
        if instr == "+":
            return sum(line)
        if instr == "*":
            return prod(line)

if __name__ == "__main__":
    with open('06.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    crusher = Crusher(lines)
    crusher.part_1()
    crusher.part_2()
