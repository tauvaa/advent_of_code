import os
from os.path import dirname
from functools import reduce


def get_data():
    with open(os.path.join(dirname(__file__), "data.txt")) as f:
        data = [[x for x in list(line) if x.strip() != ""] for line in f]
    return data


class Grid:
    def __init__(self) -> None:
        self.data = get_data()
        self.num_rows = len(self.data)
        self.num_cols = len(self.data[0])

    def get_grid_point(self, point):
        row, col = point
        if row > self.num_rows - 1 or row < 0:
            return None
        if col > self.num_cols - 1 or col < 0:
            return None

        return self.data[row][col]

class Plot:
    grid = Grid()

    def __init__(self, point) -> None:
        self.point = point
        self.region = self.grid.get_grid_point(point)
        self._get_point_perimeter()

    def __repr__(self) -> str:
        return f"({self.region}, {self.perimeter_points})"

    def _get_point_perimeter(self):
        self.perimeter_points = 0
        row, col = self.point
        offsets = [
            (i, j)
            for i in range(-1, 2)
            for j in range(-1, 2)
            if (i == 0 or j == 0) and i != j
        ]
        for row_offset, col_offset in offsets:
            if (
                self.grid.get_grid_point((row + row_offset, col + col_offset))
                != self.region
            ):
                self.perimeter_points += 1


def get_ploted_grid():
    grid = Grid()
    regions = {}
    to_ret = []
    for i in range(grid.num_rows):
        to_app = []
        for j in range(grid.num_cols):
            plot = Plot((i, j))
            if plot.region not in regions:
                regions[plot.region] = {"area": 0, "perimeter": 0}
            regions[plot.region]["area"] += 1
            regions[plot.region]["perimeter"] += plot.perimeter_points

        to_ret.append(to_app)
    return to_ret, regions


def map_regions(point, point_set):
    grid = Grid()
    row, col = point
    adjacent_points = [
        (row + row_offset, col + col_offset)
        for row_offset in range(-1, 2)
        for col_offset in range(-1, 2)
        if row_offset != col_offset and (row_offset == 0 or col_offset == 0)
    ]
    for p in adjacent_points:
        if p not in point_set and grid.get_grid_point(p) == grid.get_grid_point(point):
            point_set.add(p)
            map_regions(p, point_set)
def calculate_price(point_region):
    perimeter = 0
    area = len(point_region)
    for p in point_region:
        plot = Plot(p)
        perimeter += plot.perimeter_points
    return perimeter * area

if __name__ == "__main__":
    grid = Grid()
    point_set = set()
    point_regions = []
    all_points = [(i, j) for i in range(grid.num_rows) for j in range(grid.num_cols)] 
    for point in all_points:
        if point not in point_set:
            new_point_set = set()
            new_point_set.add(point)
            map_regions(point, new_point_set)
            point_set = point_set.union(new_point_set)
            point_regions.append(new_point_set)


    total = 0
    for region in point_regions:

        total += calculate_price(region)
    print(total)
