def tree(store, command, pos):
    if command[:1] == "$":
        if command[2:4] == "cd":
            # /: top
            if command[5:] == "/":
                pos = ["/"]
            # .. move out
            elif command[5:] == "..":
                pos.pop()
            # change dir
            else:
                pos.append(command[5:])
        elif command[2:4] == "ls":
            pass
    else:
        if command[:3] == "dir":
            store[tuple(pos + [command.split()[-1]])] = []
            store[tuple(pos)].append([0, tuple(pos + [command.split()[-1]])])
        else:
            store[tuple(pos)].append(tuple(command.split()))

    return store, pos


with open('7.txt', 'r') as f:
    storage = {("/",): []}
    position = []
    for line in f:
        storage, position = tree(storage, line[:-1], position)

keys = list(storage.keys())
keys.sort(key=len, reverse=True)

# fill in sums
for index, key in enumerate(keys):
    if index + 1 == len(keys):
        break
    dir_sum = 0
    for k in storage[key]:
        dir_sum += int(k[0])

    storage[tuple(list(key)[:-1])][list(storage[tuple(list(key)[:-1])]).index([0, key])][0] = dir_sum

keys.sort(key=len)
sums = []
for d in keys:
    dir_sum = 0
    for n in storage[d]:
        dir_sum += int(n[0])
    sums.append((dir_sum, d))

solution1 = 0
solution2 = []
# 40'000'000 free space needed
needed = sums[0][0] - 40_000_000
for i in sums:
    if i[0] <= 100000:
        solution1 += int(i[0])
    if i[0] >= needed:
        solution2.append((int(i[0]), i[1]))
solution2.sort()

print(f"total size: {sums[0][0]}")
print(f"every directory <= 100'000 summed: {solution1}")
print(f"free space needed {needed}")
print(f"delete directory at {solution2[0][1]} with size: {solution2[0][0]} to free enough space")
