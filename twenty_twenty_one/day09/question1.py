import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [list(map(int, list(x.strip()))) for x in f]
    return data


class HMap:
    def __init__(self, data) -> None:
        self.data = data
        self.max_row = len(data)
        self.max_col = len(data[0])
        self.points = [
            (i, j) for i in range(self.max_row) for j in range(self.max_col)
        ]

    def check_around(self, point):
        i, j = point
        all_points = []

        if i + 1 < self.max_row:
            all_points.append(self.data[i + 1][j])
        if i - 1 >= 0:
            all_points.append(self.data[i - 1][j])

        if j + 1 < self.max_col:
            all_points.append(self.data[i][j + 1])
        if j - 1 >= 0:
            all_points.append(self.data[i][j - 1])
        if all([self.data[i][j] < x for x in all_points]):
            return True
        return False

    def run(self):
        low_points = []
        for p in self.points:
            if self.check_around(p):
                low_points.append(self.data[p[0]][p[1]] + 1)
        print(sum(low_points))


if __name__ == "__main__":
    data = get_data()
    hmap = HMap(data)
    hmap.run()
