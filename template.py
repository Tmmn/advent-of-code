from utils import runner


class New:

    def __init__(self):
        pass

    @runner
    def part_1(self):
        pass


if __name__ == "__main__":
    with open('ex.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

