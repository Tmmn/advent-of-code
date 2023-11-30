class Rope:

    def __init__(self):
        self.x, self.y = (None, None)

    def check_close(self, other):
        if self.x - 1 == other.x and self.y + 1 == other.y:  # up left
            return True
        elif self.x == other.x and self.y + 1 == other.y:  # up middle
            return True
        elif self.x + 1 == other.x and self.y + 1 == other.y:  # up right
            return True
        elif self.x - 1 == other.x and self.y == other.y:  # left
            return True
        elif self.x == other.x and self.y == other.y:  # same
            return True
        elif self.x + 1 == other.x and self.y == other.y:  # right
            return True
        elif self.x - 1 == other.x and self.y - 1 == other.y:  # down left
            return True
        elif self.x == other.x and self.y - 1 == other.y:  # down middle
            return True
        elif self.x + 1 == other.x and self.y - 1 == other.y:  # down right
            return True
        else:
            return False


class Head(Rope):
    def __init__(self, position):
        super().__init__()
        self.x, self.y = position

    def do_checks(self):
        if not self.check_close(T1):
            T1.follow(H)
        if not T1.check_close(T2):
            T2.follow(T1)
        if not T2.check_close(T3):
            T3.follow(T2)
        if not T3.check_close(T4):
            T4.follow(T3)
        if not T4.check_close(T5):
            T5.follow(T4)
        if not T5.check_close(T6):
            T6.follow(T5)
        if not T6.check_close(T7):
            T7.follow(T6)
        if not T7.check_close(T8):
            T8.follow(T7)
        if not T8.check_close(T9):
            T9.follow(T8)

    def up(self):
        # change y + 1, make check and if false do Tail follow
        self.y += 1
        self.do_checks()

    def left(self):
        # change x - 1, make check and if false do Tail follow
        self.x -= 1
        self.do_checks()

    def right(self):
        # change x + 1, make check and if false do Tail follow
        self.x += 1
        self.do_checks()

    def down(self):
        # change y - 1, make check and if false do Tail follow
        self.y -= 1
        self.do_checks()


class Tail(Rope):
    def __init__(self, position):
        super().__init__()
        self.x, self.y = position
        self.trail = [(self.x, self.y)]

    def follow(self, other):
        # move diagonally when not close and y is different
        # move towards head when not close and y is same
        # mark new coordinate in self.trail
        old_x, old_y = self.x, self.y
        if self.y == other.y:
            self.x += 1
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            self.x -= 2
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            raise Warning("Error when following on y axis (follow 1)")
        elif self.x == other.x:
            self.y += 1
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            self.y -= 2
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            raise Warning("Error when following on x axis (follow 2)")
        else:
            # up left and right
            self.y += 1
            self.x -= 1
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            self.x += 2
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            self.x, self.y = (old_x, old_y)
            # down left and right
            self.y -= 1
            self.x -= 1
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            self.x += 2
            if other.check_close(self):
                self.trail.append((self.x, self.y))
                return
            raise Warning("Error when following diagonally (follow 3)")


H = Head((0, 0))
T1 = Tail((0, 0))
T2 = Tail((0, 0))
T3 = Tail((0, 0))
T4 = Tail((0, 0))
T5 = Tail((0, 0))
T6 = Tail((0, 0))
T7 = Tail((0, 0))
T8 = Tail((0, 0))
T9 = Tail((0, 0))

with open('9.txt', 'r') as f:
    for line in f:
        direction, iterations = line[:-1].split()
        for i in range(int(iterations)):
            if direction == "U":
                H.up()
            elif direction == "L":
                H.left()
            elif direction == "R":
                H.right()
            elif direction == "D":
                H.down()

print(f"The Head is at x = {H.x} and y = {H.y}")
print()
print(f"Tail 1 is at x = {T1.x} and y = {T1.y}")
print(f"Tail 1 visited {len(set(T1.trail))} positions at least once. (solution for Part 1)")
print()
print(f"The last Tail (tail9) is at x = {T9.x} and y = {T9.y}")
print(f"Tail 9 visited {len(set(T9.trail))} positions at least once. (solution for Part 2)")
