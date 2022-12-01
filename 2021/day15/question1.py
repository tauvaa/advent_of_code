import os
import numpy as np


# np.lin
# np.dot(a, b)
# np.li


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [l.strip() for l in f]
    data = list(map(list, data))
    data = [list(map(int, x)) for x in data]
    return data


class Grid:
    def __init__(self, data):
        self.grid = data
        self.max_x = len(data[0])
        self.max_y = len(data)
        self.current_point = (0, 0)
        self.path = []
        self.finsihed = False

    def get_value(self, row, column):
        return self.grid[row][column]

    def check_right(self):
        x, y = self.current_point
        return self.get_value(x + 1, y)

    def check_down(self):
        x, y = self.current_point
        return self.get_value(x, y + 1)

    def step_down(self):
        x, y = self.current_point
        self.current_point = (x, y + 1)
        self.path.append(self.current_point)

    def step_right(self):
        x, y = self.current_point
        self.current_point = (x + 1, y)
        self.path.append(self.current_point)

    def __str__(self):
        grid = ["".join([str(x) for x in y]) for y in self.grid]
        grid = "\n".join(grid)
        return grid

    def step(self):
        x, y = self.current_point
        if x == self.max_x - 1 and y == self.max_y - 1:
            self.finsihed = True
            return
        right_point, down_point = None, None
        if x + 1 < self.max_x:
            right_point = self.check_right()
        if y + 1 < self.max_y:
            down_point = self.check_down()

        if right_point is None:
            self.step_down()
            return
        if down_point is None:
            self.step_right()
            return
        if right_point > down_point:
            self.step_down()
            return

        if right_point <= down_point:

            self.step_right()
            return


def print_grid(data):
    data = "\n".join([",".join([str(y) for y in x]) for x in data])
    print(data)
    return data


def trim_grid(size, data, reverse=True):
    if reverse:
        tdata = data[-size:]
        to_ret = []
        for x in tdata:
            to_ret.append(x[-size:])
        return to_ret
    else:

        tdata = data[0:size]
        to_ret = []
        for x in tdata:
            to_ret.append(x[0:size])
        return to_ret


def get_out_cords(grid):
    upper = [(0, i) for i in range(len(grid))]
    side = [(i, 0) for i in range(1, len(grid))]
    return side + upper


def get_outer(grid):
    upper = grid[0]
    side = [x[0] for x in grid]
    return upper, side


def all_paths(grid, start_point, min_risk):
    all_paths = []
    risks = [min_risk]

    def walk_path(point, grid, previous="", current_score=0, path=[]):

        valid_steps = []
        x, y = point
        current_score += grid[x][y]
        min_risk = min(risks) if len(risks) > 0 else None
        if point in path or (min_risk is not None and min_risk < current_score):
            print(current_score, min_risk, len(path))
            return

        if x - 1 >= 0 and previous != "right":
            valid_steps.append("left")
        if x + 1 < len(grid[0]) and previous != "left":
            valid_steps.append("right")
        if y - 1 >= 0 and previous != "down":
            valid_steps.append("up")
        if y + 1 < len(grid) and previous != "up":
            valid_steps.append("down")
        if len(valid_steps) == 0 or point == (len(grid) - 1, len(grid[0]) - 1):
            all_paths.append(path)
            risks.append(current_score)

        else:
            for p in valid_steps:
                if p == "right":
                    new_point = (x + 1, y)
                elif p == "left":
                    new_point = (x - 1, y)
                elif p == "down":
                    new_point = (x, y + 1)
                elif p == "up":
                    new_point = (x, y - 1)
                walk_path(
                    new_point,
                    grid,
                    p,
                    current_score,
                    path + [point],
                )

    walk_path(start_point, grid)
    return all_paths, risks


def get_valid_points(grid, point, previous_point):
    max_row, max_column = len(grid), len(grid[0])
    row, column = point
    valid_points = []
    if row + 1 < max_row:
        valid_points.append((row + 1, column))
    if row - 1 >= 0:
        valid_points.append((row - 1, column))
    if column + 1 < max_column:
        valid_points.append((row, column + 1))
    if column - 1 >= 0:
        valid_points.append((row, column - 1))
    if previous_point in valid_points:
        valid_points.pop(valid_points.index(previous_point))
    return valid_points


class Distances:
    def __init__(self, dimensions):
        self.distances = [
            [None for _ in range(dimensions)] for _ in range(dimensions)
        ]

    def get_distance(self, point):

        row, column = point
        return self.distances[row][column]

    def set_distance(self, point, value):
        row, column = point
        self.distances[row][column] = value


def main(data):
    distances = Distances(len(data))
    point = (0, 0)
    unvisited_nodes = [
        (i, j) for i in range(len(data)) for j in range(len(data))
    ]

    def get_grid_value(point):
        x, y = point
        return data[x][y]
    distances.set_distance(point, 0)

    def visit_node(node):
        valid_points = get_valid_points(data, node, None)
        print(valid_points)
        valid_points = [x for x in valid_points if x in unvisited_nodes]
        print(valid_points)
        current_distance = distances.get_distance(node) or 0

        for v in valid_points:
            added_distance = get_grid_value(v)
            point_distance = added_distance + current_distance
            point_current_distance = distances.get_distance(v)
            if (
                point_current_distance is None
                or point_current_distance > point_distance
            ):

                distances.set_distance(v, point_distance)
        unvisited_nodes.pop(unvisited_nodes.index(node))

    while len(unvisited_nodes) > 0:

        visit_node(unvisited_nodes[0])
        # print_grid(distances.distances)
        # print("="*100)
    print_grid(distances.distances)
    


if __name__ == "__main__":

    data = get_data()
    # data = trim_grid(10, data, False)
    main(data)
