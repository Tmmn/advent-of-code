import time


class BoatRace:
    def __init__(self, races):
        times1 = races[0].split(":")[1].split()
        times1 = [int(t.strip()) for t in times1]
        distances1 = races[1].split(":")[1].split()
        distances1 = [int(distance.strip()) for distance in distances1]
        self.race_stats1 = [times1, distances1]

        time2 = int(races[0].split(":")[1].strip().replace(" ", ""))
        distance2 = int(races[1].split(":")[1].strip().replace(" ", ""))
        self.race_stats2 = [time2, distance2]

    def part1_wining_time(self):
        winning_button_times = []
        for i, race_time in enumerate(self.race_stats1[0]):
            winning = []
            for button_pressed in range(race_time+1):
                distance = button_pressed*(race_time-button_pressed)
                if distance > self.race_stats1[1][i]:
                    winning.append(button_pressed)
            winning_button_times.append(winning)
        return [len(button) for button in winning_button_times]

    def part2_wining_time(self):
        winning_button_times = []
        for button_pressed in range(self.race_stats2[0] + 1):
            distance = button_pressed * (self.race_stats2[0] - button_pressed)
            if distance > self.race_stats2[1]:
                winning_button_times.append(button_pressed)
        return len(winning_button_times)


if __name__ == "__main__":
    with open('06.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    boat_race = BoatRace(lines)

    start_time1 = time.perf_counter_ns()
    result1 = boat_race.part1_wining_time()
    product1 = 1
    for entry in result1:
        product1 *= entry
    end_time1 = time.perf_counter_ns()
    print(f"Part 1: result is {product1} (in {end_time1 - start_time1}ns)")

    start_time2 = time.perf_counter()
    result2 = boat_race.part2_wining_time()
    end_time2 = time.perf_counter()
    print(f"Part 2: result is {result2} (in {end_time2-start_time2}s)")
