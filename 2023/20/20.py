import time


def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(1e-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper


class MachineNetwork:
    def __init__(self, network):
        self.__network = network.copy()
        # name: (None, "flip", "conj"), [target_names], state low/high->0/1 (for conj memory dict)
        self.modules = {"button": ["but", ["broadcaster"], 0]}
        for module in network:
            name, target = module.split("->")
            # broadcaster
            if name.strip() == "broadcaster":
                self.modules["broadcaster"] = ["broad", target.strip().split(", "), 0]
            # conjunction
            elif "&" in name:
                self.modules[name.strip().strip("&")] = ["conj", target.strip().split(", "), {}]
            # flip-flop
            elif "%" in name:
                self.modules[name.strip().strip("%")] = ["flip", target.strip().split(", "), 0]

        for module in list(self.modules.keys()):
            for target in self.modules[module][1]:
                if target not in self.modules:
                    self.modules[target] = [None, None, None]
                if self.modules[target][0] == "conj":
                    self.modules[target][2][module] = 0

    @runner
    def count_pulses(self):
        count = {0: 0, 1: 0}
        queue = []
        for _ in range(1000):
            queue.append(["button", "button", 0])
            self.evaluation(queue, count)
        # print(f"end state: {self.modules}")
        return f"low {count[0]}, high {count[1]}: {count[0] * count[1]}"

    def button_module(self, counter, queue):
        queue.append(["broadcaster", 0])
        # button pressed
        counter[0] += 1
        return queue, "button", counter

    def evaluation(self, queue, pulses):
        if not queue:
            return pulses
        module, sender, pulse = queue.pop(0)
        if self.modules[module][0] is None:
            return self.evaluation(queue, pulses)
        if self.modules[module][0] == "conj":
            self.modules[module][2][sender] = pulse
        assert hasattr(self, self.modules[module][0]), f"No type named {self.modules[module][0]} known"
        happened, pulse = getattr(self, self.modules[module][0])(self.modules[module][2], pulse)
        if happened:
            if self.modules[module][0] == "flip":
                self.modules[module][2] = pulse
            # Does not work for Part 2 :(
            # if "rx" in self.modules[module][1] and pulse == 0:
            #     raise Exception
            queue.extend([[target, module, pulse] for target in self.modules[module][1]])
            pulses[pulse] += len(self.modules[module][1])
        return self.evaluation(queue, pulses)

    @staticmethod
    def flip(state, pulse):
        if state == 0 and pulse == 0:
            return 1, 1
        elif state == 1 and pulse == 0:
            return 1, 0
        elif pulse == 1:
            return 0, pulse
        else:
            raise NotImplementedError

    @staticmethod
    def conj(signals, pulse):
        if all(signals.values()):
            return 1, 0
        return 1, 1

    @staticmethod
    def but(state, pulse):
        return 1, 0

    @staticmethod
    def broad(state, pulse):
        return 1, pulse

    def restore_modules(self):
        self.__init__(self.__network)


if __name__ == "__main__":
    with open('20.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    desert_machine_park = MachineNetwork(lines)
    desert_machine_park.count_pulses()
