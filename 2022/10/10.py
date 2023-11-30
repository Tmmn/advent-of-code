def addx(plus_x):
    global x
    global cycle
    duration = 2
    for i in range(duration):
        cycle += 1
        cycle_printer()
        draw()
    else:
        x += plus_x


def noop():
    global cycle
    duration = 1
    for i in range(duration):
        cycle += 1
        cycle_printer()
        draw()


def cycle_printer():
    global cycle
    global x
    if cycle == 20 or cycle == 60 or cycle == 100 or cycle == 140 or cycle == 180 or cycle == 220:
        strength.append(cycle * x)


def draw():
    global drawing
    global minus
    if cycle - minus == x or cycle - minus == x + 2 or cycle - minus == x + 1:
        drawing += "#"
    else:
        drawing += "."

    if cycle == 40:
        minus = 40
    elif cycle == 80:
        minus = 80
    elif cycle == 120:
        minus = 120
    elif cycle == 160:
        minus = 160
    elif cycle == 200:
        minus = 200
    elif cycle == 240:
        minus = 240

    if cycle == 40 or cycle == 80 or cycle == 120 or cycle == 160 or cycle == 200 or cycle == 240:
        drawing += "\n"


minus = 0
cycle = 0
x = 1
strength = []
drawing = ""
with open('10.txt', 'r') as f:
    for line in f:
        instruction = line[:-1].split()
        if instruction[0] == "noop":
            noop()
        elif instruction[0] == "addx":
            addx(int(instruction[1]))

print(f"sum of all signal strengths combined: {sum(strength)}")
print()
print(drawing)
