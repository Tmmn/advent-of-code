from utils import runner

class Paver:

    def __init__(self, floor_plan):
        self.plan = [tuple(map(int, line.split(","))) for line in floor_plan]

    @runner
    def part_1(self):
        max_area = 0
        for i in range(len(self.plan)):
            for j in range(i + 1, len(self.plan)):
                x1, y1 = self.plan[i]
                x2, y2 = self.plan[j]
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > max_area:
                    max_area = area
        return max_area

    @runner
    def part_2(self):
        n = len(self.plan)
        max_area = 0
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = self.plan[i]
                x2, y2 = self.plan[j]
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                # skip if area is smaller than the previously calculated valid max area
                if area <= max_area:
                    continue
                # Does the polygon slice through this rectangle?
                if self.edges_intersect_interior(x1, x2, y1, y2):
                    continue
                # Is the center of the rectangle actually inside the polygon?
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                if not self.point_in_polygon(cx, cy):
                    continue
                max_area = area
        return max_area

    def point_in_polygon(self, px, py):
        inside = False
        # Check each edge of the big polygon
        for i in range(len(self.plan)):
            vx1, vy1 = self.plan[i]
            vx2, vy2 = self.plan[(i + 1) % len(self.plan)]
            # one endpoint of the edge is above, the other below py
            # horizontal lines are skipped
            if (vy1 > py) != (vy2 > py):
                if px < vx1:
                    inside = not inside
        return inside

    def edges_intersect_interior(self, rx1, rx2, ry1, ry2):
        # Normalize rectangle boundaries
        min_x, max_x = min(rx1, rx2), max(rx1, rx2)
        min_y, max_y = min(ry1, ry2), max(ry1, ry2)
        # Check each edge of the big polygon
        for i in range(len(self.plan)):
            vx1, vy1 = self.plan[i]
            vx2, vy2 = self.plan[(i + 1) % len(self.plan)]
            # Case 1: Vertical edge
            if vx1 == vx2:
                # Check if this vertical line cuts through the rectangle horizontally
                # => strictly between left and right sides, not touching boundaries
                if min_x < vx1 < max_x:
                    # Now check if the edge overlaps the rectangle's y-range
                    edge_ymin, edge_ymax = min(vy1, vy2), max(vy1, vy2)
                    # Intervals [min_y, max_y] and [edge_ymin, edge_ymax] overlap if:
                    # max(starts) < min(ends), meaning they share more than just a boundary point
                    if max(min_y, edge_ymin) < min(max_y, edge_ymax):
                        return True  # This edge cuts through the rectangle
            # Case 2: Horizontal edge
            else:
                # Check if this horizontal line cuts through the rectangle vertically
                # (strictly between top and bottom, not touching boundaries)
                if min_y < vy1 < max_y:
                    # Now check if the edge overlaps the rectangle's x-range
                    edge_xmin, edge_xmax = min(vx1, vx2), max(vx1, vx2)
                    # Check for interval overlap (more than just boundary touch)
                    if max(min_x, edge_xmin) < min(max_x, edge_xmax):
                        return True
        return False

if __name__ == "__main__":
    with open('09.txt', 'r') as source:
        lines = [row[:-1] for row in source.readlines()]
    paver = Paver(lines)
    paver.part_1()
    paver.part_2()
