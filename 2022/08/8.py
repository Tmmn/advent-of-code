def horizontal_check(tree_line, output_line):
    height = 0
    out = output_line.copy()
    for ind, tree in enumerate(tree_line):
        if ind == 0 or ind + 1 == len(tree_line):
            out[ind] = 1
            height = tree
        elif tree > height:
            height = tree
            if out[ind] == 0:
                out[ind] = 1
    return out


# build forest
forest = []
with open('8.txt', 'r') as f:
    for index, i in enumerate(f):
        forest.append([])
        for k in i[:-1]:
            forest[index].append(int(k))
        if index == 0:
            length = len(i[:-1])
        if index > 0 and len(i[:-1]) != length:
            raise Warning("different length found!")
if length < 3 or len(forest) < 3:
    raise Warning("forest to small for calculation, all trees are visible")

# create list to mark visible trees
forest_yellow_vest = [[0]*length for x in range(len(forest))]
forest_yellow_vest_back = forest_yellow_vest.copy()
forest_yellow_vest_rotate = [[0]*len(forest) for x in range(length)]
forest_yellow_vest_rotate_back = forest_yellow_vest_rotate.copy()
forest_scenic = forest_yellow_vest.copy()

# rotate forest for vertical analysis
forest_rotate = []
for m in range(length):
    line = []
    for n in range(len(forest)):
        line.append(forest[n][m])
    forest_rotate.append(line)

# horizontal normal
for idx, treeline in enumerate(forest):
    if idx == 0 or idx + 1 == len(forest):
        forest_yellow_vest[idx] = [1 for i in range(length)]
    else:
        # forward
        forest_yellow_vest[idx] = horizontal_check(treeline, forest_yellow_vest[idx])
        # backward
        forest_yellow_vest_back[idx] = horizontal_check(treeline[::-1], forest_yellow_vest_back[idx])

# horizontal rotate
for ix, rot_treeline in enumerate(forest_rotate):
    if ix == 0 or ix + 1 == len(forest_rotate):
        continue
    else:
        # forward
        forest_yellow_vest_rotate[ix] = horizontal_check(rot_treeline, forest_yellow_vest_rotate[ix])
        # backward
        forest_yellow_vest_rotate_back[ix] = horizontal_check(rot_treeline[::-1], forest_yellow_vest_rotate_back[ix])

# merge rotated tree marker lists
for q, l in enumerate(forest_yellow_vest_rotate):
    forest_yellow_vest_rotate_back[q].reverse()
    for b, o in enumerate(l):
        if forest_yellow_vest_rotate[q][b] == 0 and forest_yellow_vest_rotate_back[q][b] == 1:
            forest_yellow_vest_rotate[q][b] = forest_yellow_vest_rotate_back[q][b]

# rotate rotated tree marker list for merging
forest_yellow_vest_rotate_rotate_again = []
for m in range(len(forest_yellow_vest_rotate)):
    line = []
    for n in range(len(forest_yellow_vest_rotate[0])):
        line.append(forest_yellow_vest_rotate[n][m])
    forest_yellow_vest_rotate_rotate_again.append(line)

# merge all tree marker lists
for c, t in enumerate(forest_yellow_vest):
    forest_yellow_vest_back[c].reverse()
    for co, tr in enumerate(t):
        if forest_yellow_vest[c][co] == 0 and forest_yellow_vest_back[c][co] == 1:
            forest_yellow_vest[c][co] = forest_yellow_vest_back[c][co]
        if forest_yellow_vest[c][co] == 0 and forest_yellow_vest_rotate_rotate_again[c][co] == 1:
            forest_yellow_vest[c][co] = forest_yellow_vest_rotate_rotate_again[c][co]

# count trees
tree_counter = 0
for line in forest_yellow_vest:
    for trees in line:
        if trees == 1:
            tree_counter += 1

border = (2 * length) + (2 * len(forest)) - 4
print(f"amount of trees in border: {border}")
print(f"sum of all visible trees: {tree_counter}")

# calculate scenic score and fill in forest_scenic list
for u, rr in enumerate(forest):
    for z, h in enumerate(rr):
        scenic_up = 0
        scenic_down = 0
        scenic_left = 0
        scenic_right = 0
        other_tree = -1
        y = 1
        # up
        while other_tree < h:
            if u - y < 0:
                break
            else:
                other_tree = forest[u - y][z]
                scenic_up += 1
                y += 1
        # down
        other_tree = -1
        y = 1
        while other_tree < h:
            if u + y > len(forest) - 1:
                break
            else:
                other_tree = forest[u + y][z]
                scenic_down += 1
                y += 1
        # left
        other_tree = -1
        y = 1
        while other_tree < h:
            if z - y < 0:
                break
            else:
                other_tree = forest[u][z - y]
                scenic_left += 1
                y += 1
        # right
        other_tree = -1
        y = 1
        while other_tree < h:
            if z + y > len(forest) - 1:
                break
            else:
                other_tree = forest[u][z + y]
                scenic_right += 1
                y += 1
        forest_scenic[u][z] = scenic_up * scenic_down * scenic_left * scenic_right

print(f"the highest scenic score is: {max([max(ttt) for ttt in forest_scenic])}")
