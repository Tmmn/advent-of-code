class Schematic:
    def __init__(self, schematic):
        self.grid = schematic
        self.used_parts = None
        self.ratios = None
        self.all_numbers = self._get_numbers()

    def _get_numbers(self):
        nums = {}
        for y, line in enumerate(self.grid):
            for x, dot in enumerate(line):
                if self._is_number(dot):
                    complete_num, coords = self._complete_number((x, y))
                    for i in coords:
                        nums[i] = complete_num
        return nums

    @staticmethod
    def _is_special(c):
        return not (c.isalpha() or c.isdigit() or c == '.')

    @staticmethod
    def _is_number(c):
        return c.isdigit()

    def _complete_number(self, coord):
        # search left and right of coord to complete number
        start_coord = coord
        complete_num = []
        complete_coords = []
        # go left
        dot = self.grid[coord[1]][coord[0]]
        while self._is_number(dot):
            complete_num.insert(0, dot)
            complete_coords.append(coord)
            coord = (coord[0]-1, coord[1])
            try:
                dot = self.grid[coord[1]][coord[0]]
            except IndexError:
                dot = "."
        # go right
        coord = (start_coord[0] + 1, start_coord[1])
        try:
            dot = self.grid[coord[1]][coord[0]]
        except IndexError:
            dot = "."
        while self._is_number(dot):
            complete_num.append(dot)
            complete_coords.append(coord)
            coord = (coord[0]+1, coord[1])
            try:
                dot = self.grid[coord[1]][coord[0]]
            except IndexError:
                dot = "."
        return_num = 0
        for i in complete_num:
            return_num *= 10
            return_num += int(i)
        return return_num, complete_coords

    def _adjacent_nums(self, coord):
        # coord: x, y
        return_nums = []
        known_coords = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (coord[0] + x, coord[1] + y) in known_coords:
                    continue
                try:
                    dot = self.grid[coord[1] + y][coord[0] + x]
                except IndexError:
                    continue
                if self._is_number(dot):
                    num, num_coords = self._complete_number((coord[0] + x, coord[1] + y))
                    # print(f"adding {num}, adjacent x:{x} y:{y} to {self.grid[coord[1]][coord[0]]} at {coord}")
                    known_coords.extend(num_coords)
                    return_nums.append(num)
        return return_nums

    def missing_parts(self):
        self.used_parts = []
        for y, line in enumerate(self.grid):
            for x, dot in enumerate(line):
                if self._is_special(dot):
                    adj_nums = self._adjacent_nums((x, y))
                    for i in adj_nums:
                        self.used_parts.append(i)

    def gears(self):
        self.ratios = []
        for y, line in enumerate(self.grid):
            for x, dot in enumerate(line):
                if dot == "*":
                    adj_nums = self._adjacent_nums((x, y))
                    if len(adj_nums) == 2:
                        ratio = 1
                        for i in adj_nums:
                            ratio *= i
                        self.ratios.append(ratio)


if __name__ == "__main__":
    with open('03.txt', 'r') as source:
        lines = source.readlines()
    # remove newline
    grid = [ln[:-1] for ln in lines]
    gondola_schematic = Schematic(grid)
    # PART 1
    gondola_schematic.missing_parts()
    print(sum(gondola_schematic.used_parts))
    # PART 2
    gondola_schematic.gears()
    print(sum(gondola_schematic.ratios))
