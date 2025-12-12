from utils import runner

class Reactor:

    def __init__(self, devices):
        self.devices = devices
        self.device_graph = {}
        self.memo = {}

    def build_graph(self):
        graph = {}
        for line in self.devices:
            source, rest = line.split(": ")
            destinations = rest.split()
            graph[source] = destinations
        self.device_graph = graph

    @runner
    def part_1(self):
        memo = {}
        self.build_graph()
        total_path_count, _ = self.find_paths("you", "out", memo)
        return total_path_count

    def find_paths(self, current, end, memo):
        # Base case
        if current == end:
            return 1, memo
        if current in memo:
            return memo[current], memo
        if current not in self.device_graph:
            return 0, memo
        path_count = 0
        for neighbor in self.device_graph[current]:
            return_count, memo = self.find_paths(neighbor, end, memo)
            path_count += return_count
        memo[current] = path_count
        return path_count, memo

    def count_paths(self, start_node, end_node):
        memo = {}
        total_count, _ = self.find_paths(start_node, end_node, memo)
        return total_count

    @runner
    def part_2(self):
        self.build_graph()
        # Scenario A: svr -> dac -> fft -> out
        svr_to_dac = self.count_paths('svr', 'dac')
        dac_to_fft = self.count_paths('dac', 'fft')
        fft_to_out = self.count_paths('fft', 'out')
        scenario_a_total = svr_to_dac * dac_to_fft * fft_to_out

        # Scenario B: svr -> fft -> dac -> out
        svr_to_fft = self.count_paths('svr', 'fft')
        fft_to_dac = self.count_paths('fft', 'dac')
        dac_to_out = self.count_paths('dac', 'out')
        scenario_b_total = svr_to_fft * fft_to_dac * dac_to_out

        return scenario_a_total + scenario_b_total

if __name__ == "__main__":
    with open('11.txt', 'r') as file:
        lines = [row[:-1] for row in file.readlines()]
    reactor = Reactor(lines)
    reactor.part_1()
    reactor.part_2()
