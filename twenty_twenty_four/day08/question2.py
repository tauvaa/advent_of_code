import os
from collections import defaultdict
from copy import deepcopy
from itertools import combinations


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [list(x.strip()) for x in f]
    return data


class Solution:
    def __init__(self, data) -> None:
        self.data = data
        self.antena_points = defaultdict(list)
        self.max_rows = len(data)
        self.max_cols = len(data[0])
        self.antinodes = []

        self.get_antena_points()

    def get_antinodes(self, point1, point2):
        y1, x1 = point1
        y2, x2 = point2
        xdelta = x1 - x2
        ydelta = y1 - y2
        antinodes = []
        for i in range(1000):
            antinodes.extend(
                [(y1 + i * ydelta, x1 + i * xdelta), (y2 - i * ydelta, x2 - i * xdelta)]
            )

        return antinodes

    def get_antena_points(self):
        for i, j in [
            (i, j) for i in range(self.max_rows) for j in range(self.max_cols)
        ]:
            if self.data[i][j].isdigit() or self.data[i][j].isalpha():
                self.antena_points[self.data[i][j]].append((i, j))

    def solve(self):
        points = []
        for point_type, all_points in self.antena_points.items():
            for com in combinations(all_points, 2):
                points.extend(self.get_antinodes(*com))
        points = [
            x for x in points if 0 <= x[0] < self.max_rows and 0 <= x[1] < self.max_cols
        ]
        points = set(points)
        self.antinodes = points
        return points

    def __str__(self):
        data = deepcopy(self.data)
        for p1, p2 in points:
            data[p1][p2] = "#"
        to_ret = ["".join(x) for x in data]
        return "\n".join(to_ret)


if __name__ == "__main__":
    data = get_data()
    solution = Solution(data)
    points = solution.solve()
    print(len(points))
    # print(solution)
    # print(points)
