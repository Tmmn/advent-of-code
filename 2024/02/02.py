from utils import runner

class ReportCheck:

    def __init__(self, report):
        self.report = [[int(i) for i in j] for j in [i.split(" ") for i in report]]

    @runner
    def easy_check(self):
        return self.checker(0).count(True)

    @runner
    def dampened_check(self):
        return self.checker(1).count(True)

    def checker(self, dampener):
        validity_list = []
        for line in self.report:
            # easy check with no dampener
            if dampener == 0:
                if line[0] < line[1]:
                    validity_list.append(self.check_up(line)[0])
                elif line[0] > line[1]:
                    validity_list.append(self.check_down(line)[0])
            # complicated check with one dampener
            elif dampener == 1:
                up_bool, up_ind = self.check_up(line)
                down_bool, down_ind = self.check_down(line)
                for i in range(-1, 2):
                    if up_bool or down_bool:
                        break
                    up_bool, _ = self.check_up(line[:up_ind+i] + line[up_ind+i+1:])
                    down_bool, _ = self.check_down(line[:down_ind+i] + line[down_ind+i+1:])
                if up_bool or down_bool:
                    validity_list.append(True)
                else:
                    validity_list.append(False)
            else:
                raise NotImplementedError("dampening your provided amount is currently not supported :(")
        return validity_list

    @staticmethod
    def check_up(line):
        pred = line[0]
        for i, entry in enumerate(line[1:]):
            # if direction changes
            if pred > entry:
                return False, i+1
            # if distances are out of limits
            if abs(pred - entry) < 1 or abs(pred - entry) > 3:
                return False, i+1
            pred = entry
        return True, None

    @staticmethod
    def check_down(line):
        pred = line[0]
        for i, entry in enumerate(line[1:]):
            # if direction changes
            if pred < entry:
                return False, i+1
            # if distances are out of limits
            if abs(pred - entry) < 1 or abs(pred - entry) > 3:
                return False, i+1
            pred = entry
        return True, None


if __name__ == "__main__":
    with open('02.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]

    checker = ReportCheck(lines)
    checker.easy_check()
    checker.dampened_check()
