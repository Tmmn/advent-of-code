import copy


def part1(crates, instruction):
    for j in range(instruction[0]):
        if not crates[instruction[1]]:
            raise Warning("trying to take from empty row")
        crates[instruction[2]].insert(0, crates[instruction[1]][0])
        crates[instruction[1]].pop(0)
    return crates


def part2(crates, instruction):
    temp = []
    for j in range(instruction[0]):
        if not crates[instruction[1]]:
            raise Warning("trying to take from empty row")
        temp.append(crates[instruction[1]][0])
        crates[instruction[1]].pop(0)
    crates[instruction[2]] = temp + crates[instruction[2]]
    return crates


rows = 9
block = 0
crate_system = {}
instructions = []
solution1 = ""
solution2 = ""

for i in range(1, rows + 1):
    crate_system[i] = []
with open('5.txt', 'r') as f:
    for line in f:
        if line[:-1] == "":
            block = 1
            continue

        if block == 0:
            for index, i in enumerate(range(1, rows * 4, 4)):
                if line[i:i + 1] == " ":
                    continue
                try:
                    if isinstance(int(line[i:i + 1]), int):
                        continue
                except ValueError:
                    crate_system[index + 1].append(line[i:i + 1])

        else:
            numbers_from_line = []
            for t in line[:-1].split():
                try:
                    numbers_from_line.append(int(t))
                except ValueError:
                    pass
            instructions.append(numbers_from_line)

crate_system2 = copy.deepcopy(crate_system)

for instr in instructions:
    crate_system = part1(crate_system, instr)
    crate_system2 = part2(crate_system2, instr)

for i in crate_system.keys():
    try:
        solution1 += crate_system[i][0]
        solution2 += crate_system2[i][0]
    except IndexError:
        solution1 += str(i)

print(f"solution 1: {solution1}")
print(f"solution 2: {solution2}")
