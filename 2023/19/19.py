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


class MachineSorter:
    def __init__(self, puzzle_input):
        rules, parts = puzzle_input.split("\n\n")
        self.rules = {}
        for rule in rules.split("\n"):
            s, r = rule[:-1].split("{")
            r = [step.split(":") for step in r.split(",")]
            self.rules[s] = r
        self.parts = [{attribute.split("=")[0]: attribute.split("=")[1] for attribute in part.strip("{}").split(",")}
                      for part in parts.strip().split("\n")]

    @runner
    def rate_parts(self):
        accepted = []
        for part in self.parts:
            # start with each part at 'in', write functions for every expected behaviour, so we can do dynamic dispatch
            # if len of rule[index] is more than 1, check condition < or >. If len is 1, continue with specified rule
            result = self.step_through_rules(part, "in")
            if result == "A":
                accepted.append(part)

        part_sum = 0
        for part in accepted:
            part_sum += sum([int(i) for i in part.values()])
        return part_sum

    def step_through_rules(self, part, current_rule):
        if current_rule in ["A", "R"]:
            return current_rule
        for condition in self.rules[current_rule]:
            if len(condition) == 1:
                return self.step_through_rules(part, condition[0])
            elif "<" in condition[0]:
                left = int(part[condition[0].split("<")[0]])
                right = int(condition[0].split("<")[1])
                if self.smaller(left, right):
                    return self.step_through_rules(part, condition[1])
            elif ">" in condition[0]:
                left = int(part[condition[0].split(">")[0]])
                right = int(condition[0].split(">")[1])
                if self.larger(left, right):
                    return self.step_through_rules(part, condition[1])
            else:
                raise NotImplementedError(f"what to do with {condition}?")

    @staticmethod
    def smaller(arg1, arg2):
        return arg1 < arg2

    @staticmethod
    def larger(arg1, arg2):
        return arg1 > arg2


if __name__ == "__main__":
    with open('19.txt', 'r') as source:
        machine_sorter = MachineSorter(source.read())

    machine_sorter.rate_parts()
