data = [s.strip() for s in open("12.txt").readlines()]
width = len(data[0])
height = len(data)


def h(xy):
    return data[xy[1]][xy[0]]


def adj(xy1, xy2):  # from xy1, is xy2 at most one step down?
    return ord(h(xy1)) <= ord(h(xy2)) + 1


def getCoordsAndReplace(sym, newsym):
    sy = min([y for y in range(height) if sym in data[y]])
    sx = data[sy].index(sym)
    data[sy] = data[sy][:sx] + newsym + data[sy][sx+1:]
    return sx, sy


def getNeighbours(xy):
    nbrs = []
    (x, y) = xy
    if x > 0 and adj(xy, (x-1, y)):
        nbrs.append((x-1, y))
    if x < width - 1 and adj(xy, (x+1, y)):
        nbrs.append((x+1, y))
    if y > 0 and adj(xy, (x, y-1)):
        nbrs.append((x, y-1))
    if y < height - 1 and adj(xy, (x, y+1)):
        nbrs.append((x, y+1))
    return nbrs


(sx, sy) = getCoordsAndReplace('S', 'a')  # start
(ex, ey) = getCoordsAndReplace('E', 'z')  # end
olist = [(ex, ey)]  # open list - start from end 'E'
clist = []  # closed list
steps = 0  # number of steps taken so far (expansions of the open list)

while (sx, sy) not in olist:  # carry on until the start is in the open list
    steps += 1
    newolist = []
    for xy in olist:
        for n in getNeighbours(xy):
            if n not in olist and n not in clist and n not in newolist:
                newolist.append(n)
        clist.append(xy)
    olist = newolist

print("PART 1: Steps: ", steps)

olist = [(ex, ey)]  # open list - start from end 'E'
clist = []  # closed list
steps = 0  # number of steps taken so far (expansions of the open list)

while 'a' not in [h(xy) for xy in olist]:  # carry on until a square of height 'a' is in the open list
    steps += 1
    newolist = []
    for xy in olist:
        for n in getNeighbours(xy):
            if n not in olist and n not in clist and n not in newolist:
                newolist.append(n)
        clist.append(xy)
    olist = newolist

print("PART 2: Steps: ", steps)
