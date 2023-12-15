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


class Handbook:
    def __init__(self, steps):
        self.steps = steps.split(",")
        self.boxes_amount = 256
        self.boxes = {i: [] for i in range(self.boxes_amount)}
        self.lens = {}

    # PART 1
    @runner
    def sum_hash_results(self):
        steps_hashed = []
        for step in self.steps:
            steps_hashed.append(self.calc_hash(step))
        return sum(steps_hashed)

    # PART 2
    @runner
    def focusing_power(self):
        self.fill_boxes()
        focusing_powers = self.focusing_powers()
        return sum(focusing_powers)

    def fill_boxes(self):
        # {box: [{label: lens}, {label2: lens2}]}
        for step in self.steps:
            if step[-1] == "-":
                label = step[:-1]
                self.try_remove_lens(self.calc_hash(label), label)
            elif "=" in step:
                label, lens = step.split("=")
                self.update_box(self.calc_hash(label), label, lens)
            else:
                raise NotImplementedError(f"What to do with step {step}?")
        return True

    def focusing_powers(self):
        powers = []
        for box in range(self.boxes_amount):
            for i, lens in enumerate(self.boxes[box]):
                # box_nr+1 * slot * focal_length
                powers.append((box+1) * (i+1) * int(list(lens.values())[0]))
        return powers

    def update_box(self, box, label, lens):
        # search for lens
        for i, l in enumerate(self.boxes[box]):
            if label in l:
                # update lens when found
                self.boxes[box][i][label] = lens
                return True  # updated label with new lens
        # if label was not in box, insert lens after all other lenses
        self.boxes[box].append({label: lens})
        return False  # was not already in box

    def try_remove_lens(self, box, label):
        # search for lens
        for i, l in enumerate(self.boxes[box]):
            if label in l:
                # remove lens when found
                del self.boxes[box][i]
                return True
        # report when label was not found in box
        return False

    @staticmethod
    def calc_hash(string):
        current_value = 0
        for character in string:
            current_value += ord(character)
            current_value *= 17
            current_value %= 256
        return current_value


if __name__ == "__main__":
    with open('15.txt', 'r') as source:
        line = source.readline()[:-1]
    lava_facility_on_lava_island = Handbook(line)
    lava_facility_on_lava_island.sum_hash_results()
    lava_facility_on_lava_island.focusing_power()
