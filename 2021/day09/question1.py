import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
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
        print(point)
        return self.data[x][y]

    def get_risk(self, x, y):
        return data[x][y] + 1
    def check_around(self, point):
        x, y = point

    def find_basin(self, point):
        x, y = point
        print(x, y)
        print(self.get_value(point))


if __name__ == "__main__":
    data = get_data()
    mp = Map(data)
    points_to_check = [
        (x, y) for x in range(len(mp.data)) for y in range(len(mp.data[0]))
    ]
    low_points = []
    total = 0
    for p in points_to_check:
        if mp.check_point(*p):
            low_points.append(p)
    for p in low_points:
        total += mp.get_risk(*p)
    #mp.find_basin((0, 1))
    print(total)
