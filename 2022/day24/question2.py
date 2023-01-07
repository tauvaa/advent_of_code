import os
from typing import Any


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = list(map(list, f.read().splitlines()))
    return data


class Grid:
    def __init__(self, data):
        self.data = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])
        self.blizard_points = [
            (i, j, self.data[i][j])
            for i in range(self.num_rows)
            for j in range(self.num_cols)
            if self.data[i][j] not in ("#", ".")
        ]
        self.start_point: Any = (0, 1)
        self.point = self.start_point
        self.traveled_points = set()
        self.end_point = (len(data) - 1, data[len(data) - 1].index("."))
        self.wall_points = [
            (i, j)
            for i in range(self.num_rows)
            for j in range(self.num_cols)
            if (
                (i in (0, self.num_rows - 1) or j in (0, self.num_cols - 1))
                and (i, j) != self.start_point
                and (i, j) != self.end_point
            )
        ]

    def check_up(self, bliz_points):
        check_point = (self.point[0] - 1, self.point[1])

        if check_point in bliz_points:
            return True
        return False

    def check_down(self, bliz_points):
        check_point = (self.point[0] + 1, self.point[1])

        if check_point in bliz_points:
            return True
        return False

    def check_right(self, bliz_points):
        check_point = (self.point[0], self.point[1] + 1)

        if check_point in bliz_points:
            return True
        return False

    def check_left(self, bliz_points):
        check_point = (self.point[0], self.point[1] - 1)

        if check_point in bliz_points:
            return True
        return False

    def check_wait(self, bliz_points):
        x, y = self.point
        check_point = (x, y)
        if check_point in bliz_points:
            return True
        return False

    def check_around(self):
        to_ret = []
        row, col = self.point
        bliz_points = set((x[0], x[1]) for x in self.blizard_points)
        for x in self.wall_points:
            if x != self.end_point:
                bliz_points.add(x)

        if 1 <= row - 1 or self.end_point == (self.point[0] - 1, self.point[1]):
            if not self.check_up(bliz_points):
                to_ret.append("up")

        if self.num_rows - 2 >= row + 1 or self.end_point == (
            self.point[0] + 1,
            self.point[1],
        ):
            if not self.check_down(bliz_points):
                to_ret.append("down")

        if 1 <= col - 1:
            if not self.check_left(bliz_points):
                to_ret.append("left")

        if self.num_cols - 2 >= col + 1:
            if not self.check_right(bliz_points):
                to_ret.append("right")
        if not self.check_wait(bliz_points):
            to_ret.append("wait")
        return to_ret

    def move_person(self, point):
        to_ret = []
        self.point = point
        options = self.check_around()
        x, y = self.point

        for direction in options:

            if direction == "up":
                point = (x - 1, y)
                to_ret.append(point)

            if direction == "down":
                x, y = self.point
                to_ret.append((x + 1, y))

            if direction == "right":
                to_ret.append((x, y + 1))

            if direction == "left":
                to_ret.append((x, y - 1))
            if direction == "wait":
                to_ret.append((x, y))
        to_ret = list(set(to_ret))
        return to_ret

    def move_blizard(self):
        new_points = []
        for row, col, direction in self.blizard_points:
            if direction == "^":
                row -= 1
                if row < 1:
                    row = self.num_rows - 2
                new_points.append((row, col, direction))
            elif direction == "v":
                row += 1
                if row > self.num_rows - 2:
                    row = 1
                new_points.append((row, col, direction))
            elif direction == ">":
                col += 1
                if col > self.num_cols - 2:
                    col = 1
                new_points.append((row, col, direction))

            elif direction == "<":
                col -= 1
                if col < 1:
                    col = self.num_cols - 2

                new_points.append((row, col, direction))
        self.blizard_points = new_points

    def __str__(self):
        grid = []

        for i in range(self.num_rows):
            to_app = []
            for j in range(self.num_cols):

                if (i, j) in self.wall_points:
                    to_app.append("#")
                else:
                    to_app.append(".")
            grid.append(to_app)

        for h in self.blizard_points:
            x, y, direction = h
            current_point = grid[x][y]
            if current_point == ".":
                grid[x][y] = direction
            elif not current_point.isdigit():
                grid[x][y] = "2"
            else:
                grid[x][y] = str(int(current_point) + 1)
        grid[self.point[0]][self.point[1]] = "E"
        return "\n".join(["".join(row) for row in grid]) + "\n"


if __name__ == "__main__":
    data = get_data()
    grid = Grid(data)
    points = [grid.start_point]
    end_point = grid.end_point
    counter = 0
    while end_point not in points:
        grid.move_blizard()
        tpoints = []
        for p in points:
            tpoints.extend(grid.move_person(p))
        points = tpoints.copy()
        points = list(set(points))
        print(len(points))
        counter += 1
        if end_point in points:
            break

    start_point, end_point = grid.start_point, grid.end_point
    grid.end_point = start_point
    grid.start_point = end_point
    end_point = start_point
    print(grid.start_point)
    points = [grid.start_point]
    while end_point not in points:
        grid.move_blizard()
        tpoints = []
        for p in points:
            tpoints.extend(grid.move_person(p))
        points = tpoints.copy()
        points = list(set(points))
        print(len(points))
        counter += 1
        if end_point in points:
            break

    start_point, end_point = grid.start_point, grid.end_point
    grid.end_point = start_point
    grid.start_point = end_point
    end_point = start_point
    print(grid.start_point)
    print(end_point)
    points = [grid.start_point]
    while end_point not in points:
        grid.move_blizard()
        tpoints = []
        for p in points:
            tpoints.extend(grid.move_person(p))
        points = tpoints.copy()
        points = list(set(points))
        print(len(points))
        counter += 1
        if end_point in points:
            break

    print(counter)
