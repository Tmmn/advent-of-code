from math import prod
from utils import runner

class Playground:

    def __init__(self, junction_boxes):
        self.box_pos = [tuple(map(int, line.split(","))) for line in junction_boxes]

    @runner
    def part_1(self, merge_limit=10):
        pairs = self.get_closest_pairs()
        n = len(self.box_pos)
        # store parent of each box to form trees with root defining circuit
        parent = list(range(n))
        # store size of each circuit at root box
        sizes = [1] * n
        # merge until limit
        for k in range(merge_limit):
            self.union(parent, sizes, pairs[k][1], pairs[k][2])
        # get list of only circuit sizes
        final_circuit_sizes = []
        seen_roots = set()
        for i in range(n):
            root = self.find(parent, i)
            if root not in seen_roots:
                final_circuit_sizes.append(sizes[root])
                seen_roots.add(root)
        # top 3 largest circuits by num of boxes in circuit
        final_circuit_sizes.sort(reverse=True)
        top_3 = final_circuit_sizes[:3]
        return prod(top_3)

    @runner
    def part_2(self):
        pairs = self.get_closest_pairs()
        n = len(self.box_pos)
        parent = list(range(n))
        sizes = [1] * n
        distinct_circuits = n
        for _, i, j in pairs:
            if self.union(parent, sizes, i, j):
                # after each merge, the number of distinct circuits decreases by 1
                distinct_circuits -= 1
                if distinct_circuits == 1:
                    x1 = self.box_pos[i][0]
                    x2 = self.box_pos[j][0]
                    print(f"Last Merge was: Box {i} {self.box_pos[i]} and Box {j} {self.box_pos[j]}")
                    return x1 * x2
        return -1

    def get_closest_pairs(self):
        pairs = []
        n = len(self.box_pos)
        for i in range(n):
            for j in range(i + 1, n):
                p1 = self.box_pos[i]
                p2 = self.box_pos[j]
                dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
                pairs.append((dist, i, j))
        pairs.sort(key=lambda x: x[0])
        return pairs

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, sizes, i, j):
        root_i = self.find(parent, i)
        root_j = self.find(parent, j)
        if root_i != root_j:
            # Merge smaller set into larger set
            if sizes[root_i] < sizes[root_j]:
                # swap roots
                root_i, root_j = root_j, root_i
            # merge j into i
            parent[root_j] = root_i
            sizes[root_i] += sizes[root_j]
            return True  # Merged
        return False  # Already connected

if __name__ == "__main__":
    with open('08.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    playground = Playground(lines)
    playground.part_1(1000)
    playground.part_2()
