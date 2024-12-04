from utils import runner


class WordSearch:

    def __init__(self, riddle):
        self.riddle = riddle

    @runner
    def part_1(self, word):
        total_hits = 0
        for y, line in enumerate(self.riddle):
            for x, letter in enumerate(line):
                total_hits += self.forward(word, x, y)
                total_hits += self.backward(word, x, y)
                total_hits += self.up(word, x, y)
                total_hits += self.down(word, x, y)
                total_hits += self.diagonal_left_right_up(word, x, y)
                total_hits += self.diagonal_left_right_down(word, x, y)
                total_hits += self.diagonal_right_left_up(word, x, y)
                total_hits += self.diagonal_right_left_down(word, x, y)
        return total_hits

    @runner
    def part_2(self):
        hits = 0
        for y, line in enumerate(self.riddle[1:-1]):
            for x, letter in enumerate(line[1:-1]):
                if not letter == "A":
                    continue
                # y + 1 and x + 1 to correct
                top_left = self.riddle[y][x]
                top_right = self.riddle[y][x + 2]
                bottom_left = self.riddle[y + 2][x]
                bottom_right = self.riddle[y + 2][x + 2]
                if (
                        ((top_left == "M" and bottom_right == "S")
                         or
                         (top_left == "S" and bottom_right == "M"))
                        and
                        ((top_right == "M" and bottom_left == "S")
                         or
                         (top_right == "S" and bottom_left == "M"))
                ):
                    hits += 1
        return hits

    def forward(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if self.riddle[y][x + i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def backward(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if x - i >= 0 and self.riddle[y][x - i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def up(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if y - i >= 0 and self.riddle[y - i][x] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def down(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if self.riddle[y + i][x] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def diagonal_left_right_down(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if self.riddle[y + i][x + i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def diagonal_left_right_up(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if y - i >= 0 and self.riddle[y - i][x + i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def diagonal_right_left_down(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if x - i >= 0 and self.riddle[y + i][x - i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0

    def diagonal_right_left_up(self, word, x, y):
        matches = 0
        for i in range(len(word)):
            try:
                if x - i >= 0 and y - i >= 0 and self.riddle[y - i][x - i] == word[i]:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return 1 if matches == len(word) else 0


if __name__ == "__main__":
    with open('04.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    solver = WordSearch(lines)
    solver.part_1("XMAS")
    solver.part_2()
