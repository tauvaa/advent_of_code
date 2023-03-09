import os


def get_data():
    points, folds = [], []
    hitfolds = False
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        for line in f:
            if hitfolds:
                folds.append(line.strip())
            else:
                if line == "\n":
                    hitfolds = True
                else:
                    point = line.strip().split(",")
                    point = [int(x) for x in point]
                    points.append(tuple(point))
    return points, folds


class Grid:
    def __init__(self, points) -> None:
        self.points = set(points)
        self.max_cols = max([x[0] for x in self.points])
        self.max_rows = max([x[1] for x in self.points])

    def get_min_max(self):
        self.max_cols = max([x[0] for x in self.points])
        self.max_rows = max([x[1] for x in self.points])

    def fold_x(self, xval):
        """fold horizontally"""
        pass

        new_points = set()
        for point in self.points:
            if point[0] > xval:
                new_point = (2 * xval - point[0], point[1])
                new_points.add(new_point)
            else:
                new_points.add(point)
        self.points = new_points
        self.get_min_max()

    def fold_y(self, yval):
        """fold vertivally"""
        new_points = set()
        for point in self.points:
            if point[1] > yval:
                new_point = (point[0], yval - (point[1] - yval))
                new_points.add(new_point)
            else:
                new_points.add(point)
        self.points = new_points
        self.get_min_max()

    def __str__(self):
        grid = [
            ["." for _ in range(self.max_cols + 1)]
            for _ in range(self.max_rows + 1)
        ]
        for p in self.points:
            j, i = p
            grid[i][j] = "#"
        to_ret = ["".join(row) for row in grid]
        to_ret = "\n".join(to_ret)
        return to_ret

    def run_instruction(self, instruction):
        instruction = instruction.split(" ")[-1]
        axis, value = instruction.split("=")
        value = int(value)
        if axis == "y":
            self.fold_y(value)
        else:
            self.fold_x(value)


if __name__ == "__main__":
    points, folds = get_data()
    grid = Grid(points)
    for fold in folds:

        grid.run_instruction(fold)

    print(grid)
