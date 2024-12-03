import re
from utils import runner


class Memory:

    def __init__(self, content):
        self.content = "".join(content)

    @runner
    def correct_multiply(self):
        instructions = re.findall(r'mul\(\d+,\d+\)', self.content)
        multiplied_instructions = [int(i[4:-1].split(",")[0]) * int(i[4:-1].split(",")[1]) for i in instructions]
        return sum(multiplied_instructions)

    @runner
    def with_conditional_correct_multiply(self):
        instructions = re.findall(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', self.content)
        enabled = True
        values = []
        for instr in instructions:
            if instr == "do()":
                enabled = True
            elif instr == "don't()":
                enabled = False
            elif enabled:
                values.append(int(instr[4:-1].split(",")[0]) * int(instr[4:-1].split(",")[1]))
        return sum(values)

if __name__ == "__main__":
    with open('03.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    memory = Memory(lines)
    memory.correct_multiply()
    memory.with_conditional_correct_multiply()
