from utils import runner

class Kitchen:

    def __init__(self, database):
        sep = database.index("")
        self.fresh_ranges = [range(int(i.split("-")[0]), int(i.split("-")[1])+1) for i in database[:sep]]
        self.start_stop = [[int(j) for j in i.split("-")] for i in database[:sep]]
        self.valid_ids = [int(i) for i in database[sep+1:]]

    @runner
    def part_1(self):
        fresh_count = 0
        for i in self.valid_ids:
            for r in self.fresh_ranges:
                if i in r:
                    fresh_count += 1
                    break
        return fresh_count

    @runner
    def part_2(self):
        s_ranges = sorted(self.start_stop, key=lambda x: x[0])
        merged = [s_ranges[0]]
        for curr_start, curr_stop in s_ranges[1:]:
            last_start, last_stop = merged[-1]
            if curr_start <= last_stop:
                merged[-1][1] = max(last_stop, curr_stop)
            else:
                merged.append([curr_start, curr_stop])
        return sum(end - start + 1 for start, end in merged)

if __name__ == "__main__":
    with open('05.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    kitchen = Kitchen(lines)
    kitchen.part_1()
    kitchen.part_2()
