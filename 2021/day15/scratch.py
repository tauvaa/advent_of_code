import datetime as dt
import os

import numpy as np

from make_data import get_expanded_grid


def get_scratch_data():
    with open(
        os.path.join(os.path.dirname(__file__), "data", "scratchdata")
    ) as f:
        data = [l.strip() for l in f if l.strip() != ""]
    data = [[int(d) for d in r] for r in data]
    return data


def get_expanded_scratch_data():
    data = [x for x in get_expanded_grid().split("\n")]
    data = [[int(y) for y in x.strip()] for x in data if x.strip() != ""]
    return data


class Grid:
    def __init__(self, data):
        self.data = data
        self.data[0][0] = 0
        self.max_row = len(data)
        self.max_column = len(data[0])
        self.mask_array = np.zeros(shape=(self.max_row, self.max_column))
        # self.add_visit((0, 0))

    def get_point_value(self, *args):

        # if len(args) == 2:
        #     row, column = args
        # else:
        #     row, column = args[0]
        row, column = args[0]
        return self.data[row][column]

    def get_adjacent(self, *args):
        row, column = args[0]
        valid_point = []
        if row + 1 < self.max_row:
            valid_point += [(row + 1, column)]
        if row - 1 >= 0:
            valid_point += [(row - 1, column)]
        if column + 1 < self.max_row:
            valid_point += [(row, column + 1)]
        if column - 1 >= 0:
            valid_point += [(row, column - 1)]

        return valid_point

    def set_point_value(self, value, *args):
        if len(args) == 2:
            row, column = args
        else:
            row, column = args[0]
        self.data[row][column] = value

    def get_cord_min(self, array):
        # mask = np.ones(shape=(self.max_row, self.max_column))

        # for x in unvisted_points:
        #     mask[x] = 0
        array = np.array(array)
        mx = np.ma.masked_array(array, mask=self.mask_array)
        rowsize, columnsize = mx.shape
        amin = mx.argmin()
        row = int(amin / columnsize)
        column = amin % columnsize
        return (row, column)

    def add_visit(self, point):
        x, y = point
        self.mask_array[x][y] = 1

    def get_min_point(self):
        return self.get_cord_min(self.data)

    def __str__(self):
        rows = [",".join([str(y) for y in x]) for x in self.data]
        to_ret = "\n".join(rows)
        return to_ret


def run_grid(grid_data):
    unvisted_points = [
        (x, y) for x in range(len(grid_data)) for y in range(len(grid_data))
    ]
    start_point, end_point = (0, 0), (len(grid_data) - 1, len(grid_data) - 1)

    value_grid = Grid(grid_data)
    start_vals = [
        [np.inf for _ in range(len(grid_data))]
        for _ in range(len(grid_data[0]))
    ]
    accume_grid = Grid(start_vals)

    current_point = (0, 0)
    # unvisted_points.remove(current_point)
    unvisted_points = unvisted_points
    quick_points = set(unvisted_points)
    current_value = 0
    all_points = []
    counter = 0
    start_time = dt.datetime.now().timestamp()
    while current_point != end_point:
        for adjacent_point in accume_grid.get_adjacent(current_point):
            if adjacent_point not in quick_points:
                continue
            to_add = value_grid.get_point_value(adjacent_point)
            current_accume = accume_grid.get_point_value(adjacent_point)
            new_value = current_value + to_add
            if current_accume is not None:
                new_value = min(new_value, current_accume)
            accume_grid.set_point_value(new_value, adjacent_point)

        # unvisted_points.remove(current_point)
        accume_grid.add_visit(current_point)
        quick_points.remove(current_point)

        current_point = accume_grid.get_min_point()
        current_point_time = dt.datetime.now().timestamp()
        # print("current point time: ", current_point_time - for_time)
        current_value = accume_grid.get_point_value(current_point)

        # all_points.append(current_point)
        counter += 1
        # print("==" * 20)
        if counter % 100 == 0:
            end_time = dt.datetime.now().timestamp()
            print("total time: ", end_time - start_time)
            print(counter)
            print("quick points: ", len(quick_points))
            print("unvisited points: ", len(unvisted_points))
            start_time = end_time
    print(accume_grid)


def cut_data(data, size):
    to_ret = []
    for row in data[0:size]:
        to_ret.append(row[0:size])
    return to_ret


if __name__ == "__main__":
    # print(get_expanded_grid())
    data = get_expanded_scratch_data()
    # print(data)
    # data = get_scratch_data()
    # data = cut_data(data, 100)
    # grid = Grid(data)
    run_grid(data)
    # print(grid.get_point_value(1, 2))
    # print(grid.get_adjacent(0, 0))
