from utils import runner


class Printer:

    def __init__(self, queue_rules, queue):
        self.rules = queue_rules
        self.queue = [[int(i) for i in j] for j in [k.split(",") for k in queue]]
        self.pred = {}
        self.succ = {}

    @runner
    def part_1(self):
        self.parse_rules()
        correct_line_middles = []
        for line in self.queue:
            if self.check_validity(line):
                correct_line_middles.append(line[len(line) // 2])

        return sum(correct_line_middles)

    @runner
    def part_2(self):
        self.parse_rules()
        correct_line_middles = []
        for line in self.queue:
            if self.check_validity(line):
                continue
            before = []
            after = line.copy()
            while True:
                if len(after) == 0:
                    if self.check_validity(before):
                        correct_line_middles.append(before[len(before) // 2])
                        break
                    else:
                        after, before = before, after
                value = after.pop(0)
                for val in before:
                    if value in self.succ.keys() and val in self.succ[value]:
                        before.remove(val)
                        after.insert(0, val)
                for val in after:
                    if value in self.pred.keys() and val in self.pred[value]:
                        after.remove(val)
                        before.append(val)
                before.append(value)

        return sum(correct_line_middles)

    def check_validity(self, line):
        before = []
        after = line.copy()
        for _ in line:
            value = after.pop(0)
            if value not in self.succ.keys() or value not in self.pred.keys():
                before.append(value)
                continue
            if value in self.succ.keys():
                for val in before:
                    if val in self.succ[value]:
                        return False
            if value in self.pred.keys():
                for val in after:
                    if val in self.pred[value]:
                        return False
            before.append(value)
        return True

    def parse_rules(self):
        self.pred = {}
        self.succ = {}
        for rule in self.rules:
            l, r = int(rule.split("|")[0]), int(rule.split("|")[1])
            if r not in self.pred.keys():
                self.pred[r] = [l]
            else:
                self.pred[r].append(l)
            if l not in self.succ.keys():
                self.succ[l] = [r]
            else:
                self.succ[l].append(r)

if __name__ == "__main__":
    with open('05.txt', 'r') as source:
        rules = []
        updates = []
        separator = False
        for row in source:
            if row[:-1] == '':
                separator = True
            elif separator:
                updates.append(row[:-1])
            else:
                rules.append(row[:-1])

    rule_checker = Printer(rules, updates)
    rule_checker.part_1()
    rule_checker.part_2()
