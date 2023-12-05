import time

class Almanac:
    def __init__(self, s, almanac):
        # source
        self.almanac = almanac
        # list with all seeds
        self.seeds = s
        # list with all seed ranges [[seed_range_start1, seed_range_start2], [seed_range_start2, seed_range_start2]]
        self.seed_range = []
        for j in range(0, len(self.seeds), 2):
            self.seed_range.append([self.seeds[j], self.seeds[j] + self.seeds[j+1]-1])
        # dicts that show how the source and destination numbers are mapped, dict that show the sequence of conversions
        self.map, self.sequence, self.sequence_back = self._calc_map()
        # location of each seed with rules for part 1 (with performance timing)
        t_start = time.perf_counter()
        self.seed_locations_part1 = {grain: self.get_location(self.sequence, grain) for grain in self.seeds}
        t_end = time.perf_counter()
        self.part1_time = t_end - t_start

    def lowest_location_seed(self, mode=1):
        # Part 1
        seed = None
        location = 1000000
        if mode == 1:
            while seed is None:
                return_seed = self.get_seed(self.sequence_back, location)
                if return_seed in self.seeds:
                    seed = return_seed
                    break
                location += 1
        # Part 2
        elif mode == 2:
            while seed is None:
                return_seed = self.get_seed(self.sequence_back, location)
                if self._seed_range_check(return_seed):
                    seed = return_seed
                    break
                location += 1
        else:
            raise NotImplementedError(f"unknown mode {mode}")
        return seed, location

    def _seed_range_check(self, seed):
        # checks if given seed is in range according to rules for part 2
        for s_range in self.seed_range:
            if s_range[0] <= seed <= s_range[1]:
                return True
        return False

    def _calc_map(self):
        # build dictionary with {(source, destination): [list of list with conversions]}
        # build dictionary with dict that shows the order of conversions
        # build dictionary with reversed order of conversions
        con = {}
        instruction_list = []
        current = None
        for line in self.almanac:
            if not line:
                continue
            elif line[0].isdigit():
                # the destination range start, the source range start, and the range length.
                # source_start, source_end, destination_start, destination_end
                if current is None:
                    raise Exception(f"encountered mapping statements but no direction is known")
                alm_map = [int(num) for num in line.split()]
                mappings = [alm_map[1], alm_map[1] + alm_map[2]-1, alm_map[0], alm_map[0] + alm_map[2]-1]
                con[current].append(mappings)
            else:
                current = tuple(line.split()[0].split("-")[0:3:2])
                instruction_list.insert(0, current[0])
                con[current] = []
        instruction_list.insert(0, current[1])

        instruction_list_back = instruction_list[::-1]
        instructions = instruction_list[0]
        instructions_back = instruction_list_back[0]
        for i in range(1, len(instruction_list)):
            instructions = {instruction_list[i]: instructions}
        for i in range(1, len(instruction_list_back)):
            instructions_back = {instruction_list_back[i]: instructions_back}
        return con, instructions, instructions_back

    def get_location(self, sequence, start_nr):
        # search through map using the sequence until value in sequence is not dict anymore
        # returns the location for given seed
        if not isinstance(sequence, dict):
            return start_nr
        assert len(sequence.keys()) == 1, f"could not find source in sequence {sequence}"
        start = list(sequence.keys())[0]
        assert len(sequence.values()) == 1, f"could not find destination in sequence {sequence}"
        destination = list(sequence[start].keys())[0] if isinstance(sequence[start], dict) else sequence[start]
        map_key = (start, destination)
        end_nr = None
        for mapping in self.map[map_key]:
            if mapping[0] <= start_nr <= mapping[1]:
                offset = start_nr - mapping[0]
                end_nr = mapping[2] + offset
        if end_nr is None:
            end_nr = start_nr
        return self.get_location(sequence[start], end_nr)

    def get_seed(self, sequence, start_nr):
        # search through map using the sequence until value in sequence is not dict anymore
        # returns seed for given location
        if not isinstance(sequence, dict):
            return start_nr
        assert len(sequence.keys()) == 1, f"could not find source in sequence {sequence}"
        start = list(sequence.keys())[0]
        assert len(sequence.values()) == 1, f"could not find destination in sequence {sequence}"
        destination = list(sequence[start].keys())[0] if isinstance(sequence[start], dict) else sequence[start]
        map_key = (destination, start)
        end_nr = None
        for mapping in self.map[map_key]:
            if mapping[2] <= start_nr <= mapping[3]:
                offset = start_nr - mapping[2]
                end_nr = mapping[0] + offset
        if end_nr is None:
            end_nr = start_nr
        return self.get_seed(sequence[start], end_nr)


if __name__ == "__main__":
    with open('05.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    seeds = [int(seed) for seed in lines[0].split(": ")[1].split()]
    island_island = Almanac(seeds, lines[1:])
    print(f"With rules for part 1 the lowest location is: {min(island_island.seed_locations_part1.values())} "
          f"(in {island_island.part1_time}s)")
    start_time = time.perf_counter()
    seed, loc = island_island.lowest_location_seed(2)
    end_time = time.perf_counter()
    print(f"With rules for part 2 the lowest location is {loc} (for seed {seed} in {end_time-start_time}s)")
