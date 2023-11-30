# ASCII: A:65, Z:90; a:97, z:122


def part1(backpack):
    double_characters = []
    middle = len(backpack) // 2

    for i in range(65, 91):
        if chr(i) in backpack[:middle] and chr(i) in line[middle:]:
            double_characters.append((i - 38, i, chr(i)))
    for i in range(97, 123):
        if chr(i) in backpack[:middle] and chr(i) in line[middle:]:
            double_characters.append((i - 96, i, chr(i)))

    if len(double_characters) > 1:
        raise Warning("more than one double character found!")
    elif len(double_characters) == 1:
        return double_characters[0][0]
    else:
        return 0


def part2(backpack):
    double_characters = []
    for i in range(65, 91):
        if chr(i) in backpack[0] and chr(i) in backpack[1] and chr(i) in backpack[2]:
            double_characters.append((i - 38, i, chr(i)))
    for i in range(97, 123):
        if chr(i) in backpack[0] and chr(i) in backpack[1] and chr(i) in backpack[2]:
            double_characters.append((i - 96, i, chr(i)))

    if len(double_characters) > 1:
        raise Warning("more than one double character found!")
    elif len(double_characters) == 1:
        return double_characters[0][0]
    else:
        return 0


sum1 = 0
sum2 = 0
with open('3.txt', 'r') as f:
    triple_line = []
    for index, line in enumerate(f):
        sum1 += part1(line[:-1])
        triple_line.append(line[:-1])
        if (index + 1) % 3 == 0:
            sum2 += part2(triple_line)
            triple_line = []


print(f"answer for part 1: {sum1}")
print(f"answer for part 2: {sum2}")
