import re

# geklaut von @SexyCurryboy
# https://www.reddit.com/r/adventofcode/comments/zifqmh/2022_day_11_solutions/
with open("ex.txt", "r") as f:
    from_file = [line.strip() for line in f]

monkeys = {}
for index, line in enumerate(from_file):
    if line.startswith("Monkey"):
        monkeys[int(line.split()[1][:-1])] = {
            "items": [int(x) for x in re.split(": |, ", from_file[index + 1])[1:]],
            "operation": from_file[index + 2][17:],
            "test": int(from_file[index + 3].split()[3]),
            "throw true": int(from_file[index + 4][-1:]),
            "throw false": int(from_file[index + 5][-1:]),
            "inspections": 0
        }

teiler = [monkeys[x]["test"] for x in monkeys]
print(monkeys)
