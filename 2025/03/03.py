from utils import runner

class Elevator:

    def __init__(self, banks):
        self.banks = banks

    @runner
    def part_1(self):
        return sum([int(self.get_largest_subsequence(b, 2)) for b in self.banks])

    @runner
    def part_2(self):
        return sum(int(self.get_largest_subsequence(b, 12)) for b in self.banks)

    @staticmethod
    def get_largest_subsequence(seq, l):
        stack = []
        n = len(seq)

        for i, char in enumerate(seq):
            remaining_in_str = n - i
            # remove number if the current number is bigger than the last and there are enough numbers coming
            while stack and stack[-1] < char and (len(stack) + remaining_in_str) > l:
                stack.pop()
            # add the number if there is still room
            if len(stack) < l:
                stack.append(char)
        return "".join(stack)

if __name__ == "__main__":
    with open('03.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    ele = Elevator(lines)
    ele.part_1()
    ele.part_2()
