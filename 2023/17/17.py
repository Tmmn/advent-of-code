import time
from heapq import heappush, heappop
from pprint import pprint


def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(10**-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper


class CityMap:
    def __init__(self, city_map):
        self.city_map = city_map
        self.direct_max = 3

    @runner
    def best_crucible_path(self):
        # had to make drastic changes to the algorithm and now the grid printing does not work anymore
        # TODO: fix it
        graph = self.get_new_graph_from_map()
        start = (0, 0)
        goal = (len(self.city_map)-1, len(self.city_map[0])-1)
        tot_cost = self.dijkstra(graph, start, goal, 0, 3)
        # help_grid = [["."]*len(self.city_map[0]) for _ in range(len(self.city_map))]
        # direct = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">"}
        # h = goal
        # while h != start:
        #     print(f"{graph[h]["pos"]} to {graph[h]["previous"]}, {graph[h]["cost_tot"]}")
        #     help_grid[h[0]][h[1]] = direct[graph[h]["prev_direct"][0]]
        #     h = graph[h]["previous"]
        # pprint(help_grid)
        # return graph[goal]["cost_tot"]
        return tot_cost

    @runner
    def best_ultra_crucible_path(self):
        graph = self.get_new_graph_from_map()
        start = (0, 0)
        goal = (len(self.city_map)-1, len(self.city_map[0])-1)
        tot_cost = self.dijkstra(graph, start, goal, 4, 10)
        return tot_cost

    def get_new_graph_from_map(self):
        graph = {}
        for y, row in enumerate(self.city_map):
            for x, point in enumerate(row):
                graph[(y, x)] = {
                    "pos": (y, x),  # store position as tuple
                    "cost": int(point),  # store cost to reach this vertex from previous
                    "cost_tot": float('inf'),  # store total cost to reach this vertex from start
                    "previous": None,  # set previous vertex to None
                    "prev_direct": [(0, 0), 0],  # direction in which previous lies and nr of times same distance
                }
        return graph

    def dijkstra(self, graph, start, goal, min_steps, max_steps):
        tot_cost = 0
        # (tot_cost, (y, x), (dy, dx), nr_same_direction)
        q = [(tot_cost, start, (1, 0), 0), (tot_cost, start, (0, 1), 0)]
        visited = set()

        while q:
            tot_cost, pos, direction, nr_same_dir = heappop(q)
            if pos == goal:
                if nr_same_dir < min_steps:
                    continue
                break

            if (pos, direction, nr_same_dir) in visited:
                continue

            visited.add((pos, direction, nr_same_dir))
            for neigh in self._neighbors(pos):
                # neigh[0] neighbor pos, neigh[0] neighbor direction
                new_pos, new_direction = neigh
                new_cost = tot_cost + graph[new_pos]["cost"]
                # same direction? True or False
                same_dir = direction == new_direction
                # if not opposite direction and not same direction more than max_steps times
                # and not change direction if less than min steps
                if (not (direction[0] == -1*new_direction[0] and direction[1] == -1*new_direction[1]) and not
                        (same_dir and nr_same_dir >= max_steps) and not (not same_dir and nr_same_dir < min_steps)):
                    new_nr_same_dir = nr_same_dir + 1 if same_dir else 1
                    heappush(q, (new_cost, new_pos, new_direction, new_nr_same_dir))
        return tot_cost

    def _neighbors(self, coord):
        pot_neighbors = [
            ((coord[0]-1, coord[1]), (-1, 0)),
            ((coord[0]+1, coord[1]), (1, 0)),
            ((coord[0], coord[1]-1), (0, -1)),
            ((coord[0], coord[1]+1), (0, 1))]
        return [pot_neigh for pot_neigh in pot_neighbors if self._in_city(pot_neigh[0])]

    def _in_city(self, coord):
        if 0 <= coord[0] < len(self.city_map) and 0 <= coord[1] < len(self.city_map[0]):
            return True
        return False


if __name__ == "__main__":
    with open('17.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    gear_island_factory_city = CityMap(lines)
    gear_island_factory_city.best_crucible_path()
    gear_island_factory_city.best_ultra_crucible_path()
