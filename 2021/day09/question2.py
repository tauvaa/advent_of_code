import os
from functools import reduce


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [list(x.strip()) for x in f]
    data = [[int(x) for x in y] for y in data]
    return data


class Map:
    def __init__(self, data):
        self.data = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])
        self.basin_points = []

    def check_point(self, i, j):
        current_level = self.data[i][j]

        if i + 1 < self.num_rows:
            if self.data[i + 1][j] <= current_level:
                return False
        if i - 1 >= 0:
            if self.data[i - 1][j] <= current_level:
                return False
        if j + 1 < self.num_cols:
            if self.data[i][j + 1] <= current_level:
                return False
        if j - 1 >= 0:
            if self.data[i][j - 1] <= current_level:
                return False
        return True

    def get_value(self, point):
        x, y = point
        return self.data[x][y]

    def get_risk(self, x, y):
        return data[x][y] + 1

    def add_to_basin(self, point):
        point = tuple(point)

        if self.get_value(point) < 9:

            if point not in self.basin_points:
                self.basin_points.append(point)
                self.find_basin(point)
            # self.basin_points.append(tuple(point))

    def find_basin(self, point):
        x, y = point
        valid_rows = [x]
        valid_cols = [y]
        if x - 1 >= 0:
            valid_rows += [x - 1]
        if x + 1 < self.num_rows:
            valid_rows += [x + 1]
        if y - 1 >= 0:
            valid_cols += [y - 1]
        if y + 1 < self.num_cols:
            valid_cols += [y + 1]
        valid_points = [(x, y) for x in valid_rows for y in valid_cols]
        valid_points = [k for k in valid_points if k[0] == x or k[1] == y]
        for p in valid_points:
            self.add_to_basin(p)

    def check_basin_size(self, point):
        self.basin_points = []
        self.find_basin(point)
        return len(self.basin_points)


if __name__ == "__main__":
    data = get_data()
    mp = Map(data)
    points_to_check = [
        (x, y) for x in range(len(mp.data)) for y in range(len(mp.data[0]))
    ]
    low_points = []
    total = 0
    basin_sizes = []
    for p in points_to_check:
        if mp.check_point(*p):
            low_points.append(p)
    for p in low_points:
        total += mp.get_risk(*p)
        basin_sizes.append(mp.check_basin_size(p))
    basin_sizes.sort(reverse=True)
    basin_sizes[0:3]
    print(reduce(lambda x, y: x*y, basin_sizes[0:3]))

