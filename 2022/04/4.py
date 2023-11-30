
def part1(pairs):
    split_pairs = pairs.replace(",", "-").split("-")
    first_start, first_end, second_start, second_end = tuple(split_pairs)
    first = range(int(first_start), int(first_end) + 1)
    second = range(int(second_start), int(second_end) + 1)

    if set(first) <= set(second) or set(first) >= set(second):
        return 1
    else:
        return 0


def part2(pairs):
    split_pairs = pairs.replace(",", "-").split("-")
    first_start, first_end, second_start, second_end = tuple(split_pairs)
    first = range(int(first_start), int(first_end) + 1)
    second = range(int(second_start), int(second_end) + 1)

    if any(i in first for i in second):
        return 1
    else:
        return 0


sum1 = 0
sum2 = 0
with open('4.txt', 'r') as f:
    for line in f:
        sum1 += part1(line[:-1])
        sum2 += part2(line[:-1])

print(f"solution for part 1: {sum1}")
print(f"solution for part 2: {sum2}")
