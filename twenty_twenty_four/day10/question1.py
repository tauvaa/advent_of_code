import os
from collections import defaultdict


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [[int(y) if y.isdigit() else y for y in x.strip()] for x in f]
    return data


class Point:
    def __init__(self) -> None:
        self.adjacent_points = []
class Grid:
    def __init__(self) -> None:
        self.data = get_data()
        self.zeros = set()
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])
        self.path_counter = 0
        self.found_ends = set()
        self.get_zeros()

    def get_point_value(self, point):
        row, col = point
        to_ret = self.data[row][col]
        if to_ret != ".":
            return to_ret

    def get_zeros(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.get_point_value((i, j)) == 0:
                    self.zeros.add((i, j))

    def get_left(self, point):
        row, col = point
        if col - 1 >= 0:
            next_point = (row, col - 1)
            return self.get_point_value(next_point), next_point

    def get_right(self, point):
        row, col = point
        if col + 1 < self.num_cols:
            next_point = (row, col + 1)
            return self.get_point_value(next_point), next_point

    def get_up(self, point):
        row, col = point
        if row - 1 >= 0:
            next_point = (row - 1, col)
            return self.get_point_value(next_point), next_point

    def get_down(self, point):
        row, col = point
        if row + 1 < self.num_rows:
            next_point = (row + 1, col)
            return self.get_point_value(next_point), next_point
    def reset_paths(self):
        self.found_ends = set()
        self.path_counter = 0

    def take_step(self, point):
        current_value = self.get_point_value(point)
        assert current_value is not None
        left = self.get_left(point)
        right = self.get_right(point)
        up = self.get_up(point)
        down = self.get_down(point)
        for direction in (left, right, up, down):
            if direction and direction[0]:
                if direction[0] == current_value +1:
                    if direction[0] == 9 and direction[1] not in self.found_ends:
                        self.found_ends.add(direction[1])
                        self.path_counter += 1
                    else:
                        self.take_step(direction[1])


if __name__ == "__main__":
    grid = Grid()
    total = 0
    for z in grid.zeros:
        print(z)
        grid.take_step(z)
        total += grid.path_counter
        grid.reset_paths()
    print(total)

    # print(grid.zeros)
