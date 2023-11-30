with open('6.txt', 'r') as f:
    line = f.readline()

# Part 1
for index, char in enumerate(line):
    if index < 4:
        continue
    else:
        if len(set(line[index - 4: index])) == 4:
            print(f"marker for part1 found at index {index}")
            break

# Part 2
for index, char in enumerate(line):
    if index < 14:
        continue
    else:
        if len(set(line[index - 14: index])) == 14:
            print(f"marker for part2 found at index {index}")
            break
