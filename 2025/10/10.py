import re
import numpy as np
from itertools import combinations
from scipy.optimize import milp, LinearConstraint, Bounds
from utils import runner

class Factory:

    @runner
    def __init__(self, manual):
        # [(indicators, buttons), ...]
        self.manual = [
            (
                sum(1 << i for i, c in enumerate(l[l.find("[")+1:l.find("]")]) if c == "#"),
                [sum(1 << int(x) for x in b.split(",")) for b in re.findall(r'\(([\d,]+)\)', l)]
            )
            for l in manual
        ]
        # [(joltage, buttons), ...]
        self.manual2 = [
            (
                list(map(int, re.search(r'\{([\d,]+)}', l).group(1).split(','))),
                [list(map(int, b.split(","))) for b in re.findall(r'\(([\d,]+)\)', l)]
            )
            for l in manual
        ]

    @runner
    def part_1(self):
        total_presses = 0
        for t, b in self.manual:
            # Find minimum combination of buttons to match target
            found = False
            for presses in range(len(b) + 1):
                for combo in combinations(b, presses):
                    current_state = 0
                    for btn in combo:
                        current_state ^= btn
                    if current_state == t:
                        total_presses += presses
                        found = True
                        break
                if found:
                    break
        return total_presses

    @runner
    def part_2(self):
        total_presses = 0
        for target_vec, button_indices in self.manual2:
            total_presses += self._solve_scipy(button_indices, target_vec)
        return total_presses

    @staticmethod
    def _solve_scipy(buttons, target):
        n_b = len(buttons)
        n_t = len(target)

        # Rows = Joltage Counters, Cols = Buttons
        A = np.zeros((n_t, n_b))
        for col_idx, indices in enumerate(buttons):
            for row_idx in indices:
                A[row_idx, col_idx] = 1
        constraints = LinearConstraint(A, lb=target, ub=target)

        c = np.ones(n_b)
        # integrality=1 means all variables must be integers
        integrality = np.ones(n_b)
        bounds = Bounds(lb=0, ub=np.inf)
        res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)

        if res.success:
            return round(res.fun)
        return 0

if __name__ == "__main__":
    with open('10.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    factory = Factory(lines)
    factory.part_1()
    factory.part_2()
