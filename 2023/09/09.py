import time


def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(10e-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper


class OASISReport:
    def __init__(self, sensors):
        self.sensor_history = sensors

    @runner
    def report_forward(self):
        next_values = []
        for sensor in self.sensor_history:
            history = self._get_differences(sensor)
            history.reverse()
            next_values.append(self._calc_next_value(history, 0))
        return sum(next_values)

    def _calc_next_value(self, history, val):
        try:
            adder = history[1][-1]
        except IndexError:
            return val
        return self._calc_next_value(history[1:], val + adder)

    @runner
    def report_backward(self):
        previous_values = []
        for sensor in self.sensor_history:
            history = self._get_differences(sensor)
            history.reverse()
            previous_values.append(self._calc_previous_value(history, 0))
        return sum(previous_values)

    def _calc_previous_value(self, history, val):
        try:
            adder = history[1][0]
        except IndexError:
            return val
        return self._calc_previous_value(history[1:], (-1*val) + adder)

    def _get_differences(self, data):
        differences = []
        for i in range(len(data)-1):
            diff = data[i+1] - data[i]
            differences.append(diff)
        if not differences:
            raise NotImplementedError(f"could not calculate difference of {data}")
        elif differences.count(0) == len(differences):
            return [data] + [differences]
        return [data] + self._get_differences(differences)


if __name__ == "__main__":
    with open('09.txt', 'r') as source:
        lines = []
        for row in source.readlines():
            lines.append([int(num) for num in row[:-1].split()])

    oasis_below_metal_island = OASISReport(lines)
    oasis_below_metal_island.report_forward()
    oasis_below_metal_island.report_backward()
