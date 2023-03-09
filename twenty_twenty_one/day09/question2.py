import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
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

    def get_low_points(self):
        low_points = []
        for p in self.points:
            if self.check_around(p):
                low_points.append(p)
        return low_points

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
        low_points = self.get_low_points()
        low_points = [Basin(self.data, x) for x in low_points]
        all_nums = []
        for basin in low_points:
            basin.check_around(basin.point)
            all_nums.append(len(basin.checked_points))
        num = 1
        all_nums.sort(reverse=True)
        all_nums = all_nums[0:3]
        for a in all_nums:
            num *= a
        print(num)


class Basin(HMap):
    def __init__(self, data, point) -> None:
        super().__init__(data)
        self.point = point
        self.checked_points = set()

    def check_around(self, point):
        i, j = point
        to_add = set()

        if i + 1 < self.max_row:
            if (
                self.data[i + 1][j] != 9
                and (i + 1, j) not in self.checked_points
            ):
                to_add.add((i + 1, j))

        if i - 1 >= 0:
            if (
                self.data[i - 1][j] != 9
                and (i - 1, j) not in self.checked_points
            ):
                to_add.add((i - 1, j))

        if j + 1 < self.max_col:
            if (
                self.data[i][j + 1] != 9
                and (i, j + 1) not in self.checked_points
            ):
                to_add.add((i, j + 1))
        if j - 1 >= 0:
            if (
                self.data[i][j - 1] != 9
                and (i, j - 1) not in self.checked_points
            ):
                to_add.add((i, j - 1))
        self.checked_points = self.checked_points.union(to_add)
        for p in to_add:
            self.check_around(p)


if __name__ == "__main__":
    data = get_data()
    hmap = HMap(data)
    hmap.run()
