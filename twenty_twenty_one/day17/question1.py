import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip()
    print(data)
    pattern = r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)"
    m = re.match(pattern, data)
    x1, x2, y1, y2 = m.groups()
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    return [(x1, x2), (y1, y2)]


class Grid:
    def __init__(self, grid_points) -> None:
        x, y = grid_points
        self.minx, self.maxx = x
        self.miny, self.maxy = y
        self.grid_points = [
            (i, j)
            for i in range(self.minx, self.maxx + 1)
            for j in range(self.miny, self.maxy + 1)
        ]

    def shoot(self, traject):
        tx, ty = traject
        current_point = (0, 0)
        max_height = 0

        while True:
            currentx, currenty = current_point
            currentx += tx
            currenty += ty
            max_height = max(max_height, currenty)
            if tx > 0:
                tx -= 1
            if tx < 0:
                tx += 1
            ty -= 1
            current_point = (currentx, currenty)
            if currenty < self.miny:
                return False, None

            if current_point in self.grid_points:
                return True, max_height


if __name__ == "__main__":
    data = get_data()
    print(data)
    points = [(i, j) for i in range(100) for j in range(100)]
    max_height = 0
    grid = Grid(data)
    counter = 0
    for p in points:
        cond, height = grid.shoot(p)
        if cond:
            max_height = max(max_height, height)
        counter += 1
        if counter % 1000 == 0:
            print(f"count: {counter}")
    print(max_height)
