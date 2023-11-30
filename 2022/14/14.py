def normalize(instr):
    global min_x
    global min_y
    return [int(instr[0]) - min_x, int(instr[1]) - min_y]


def fill_walls(room, instruction):
    norm_left, norm_right = normalize(instruction[0]), normalize(instruction[1])
    # print(norm_left, norm_right)
    # same x, draw y
    if norm_left[0] == norm_right[0]:
        for z in range(norm_left[1], norm_right[1] + 1):
            room[z] = room[z][:norm_left[0]] + "#" + room[z][norm_left[0] + 1:]
    # same y, draw x
    elif norm_left[1] == norm_right[1]:
        hor = ""
        if norm_left[0] < norm_right[0]:
            for _ in range(norm_left[0], norm_right[0] + 1):
                hor += "#"
            room[norm_left[1]] = room[norm_left[1]][:norm_left[0]] + hor + room[norm_left[1]][norm_right[0] + 1:]
        else:
            for _ in range(norm_left[0], norm_right[0] - 1, -1):
                hor += "#"
            room[norm_left[1]] = room[norm_left[1]][:norm_right[0]] + hor + room[norm_left[1]][norm_left[0] + 1:]

    return room


def print_grid(gr):
    for l in gr:
        print(l)


def sand_check(room, sand):
    x, y = sand

    while True:
        if x < 0 or x >= len(room[0]) or y >= len(room):
            return room, False

        # down
        if y == len(room) or room[y + 1][x] == "." or y == len(room):
            y += 1
            continue
        # diagonally left
        if x == 0 or room[y + 1][x - 1] == ".":
            x -= 1
            y += 1
            continue
        # diagonally right
        if x == len(room[0]) - 1 or room[y + 1][x + 1] == ".":
            x += 1
            y += 1
            continue

        break

    room[y] = room[y][:x] + "O" + room[y][x + 1:]
    return room, True


with open('14.txt', 'r') as f:
    scans = []
    for line in f:
        scans.append([i.split(",") for i in line.strip().split(" -> ")])

# how big does the grid have to be
min_x, max_x, min_y, max_y = float("inf"), 0, 0, 0
for s in scans:
    for ss in s:
        max_x = int(ss[0]) if int(ss[0]) > max_x else max_x
        min_x = int(ss[0]) if int(ss[0]) < min_x else min_x
        max_y = int(ss[1]) if int(ss[1]) > max_y else max_y

# create grid
horizontal = ""
for _ in range(min_x, max_x + 1):
    horizontal += "."
grid1 = [horizontal for _ in range(min_y, max_y + 1)]

for s in scans:
    for ind, ss in enumerate(s):
        if ind == len(s) - 1:
            continue
        grid1 = fill_walls(grid1, [ss, s[ind + 1]])


print_grid(grid1)

sand = normalize([500, 0])
static_sand = 0
while True:
    grid1, ongoing = sand_check(grid1, sand)
    if not ongoing:
        break
    static_sand += 1

print()
print_grid(grid1)
print(f"amount of sand: {static_sand}")
