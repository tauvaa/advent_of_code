import os
import datetime as dt
import string


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [list(l.strip()) for l in f]
    return data


class Node:
    def __init__(self, node_value):
        self.neighbours = []
        self.value = node_value
        self.path_value = None

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)


class Grid:
    def __init__(self, data):
        self.grid_data = data
        self.start_point, self.end_point = self.find_start_end_points()
        self.grid = self.make_grid()
        self.unchecked = set(
            [(i, j) for i in range(len(data)) for j in range(len(data[0]))]
        )
        self.unchecked.remove(self.start_point)
        self.tentative_values = {
            (i, j): None for i in range(len(data)) for j in range(len(data[0]))
        }
        self.tentative_values[self.start_point] = 0
        self.current_value = self.start_point
        self.grid[self.current_value[0]][self.current_value[1]].path_value = 0

    def find_start_end_points(self):
        start_point, end_point = None, None
        for i in range(len(self.grid_data)):
            for j in range(len(self.grid_data[0])):
                if self.grid_data[i][j] == "S":
                    start_point = (i, j)
                    self.grid_data[i][j] = "a"
                if self.grid_data[i][j] == "E":
                    end_point = (i, j)
                    self.grid_data[i][j] = "z"
                if all(x is not None for x in (start_point, end_point)):
                    return start_point, end_point

    def check_letter(self, current, potential):
        slist = list(string.ascii_letters)
        aindex = slist.index(current)
        bindex = slist.index(potential)
        return bindex <= aindex + 1

    def make_grid(self):
        to_ret = []
        max_rows, max_cols = len(self.grid_data), len(self.grid_data[0])
        for i in range(len(self.grid_data)):

            to_app = []
            for j in range(len(self.grid_data[0])):
                n = Node(self.grid_data[i][j])
                current_value = self.grid_data[i][j]
                if j > 0:
                    if self.check_letter(
                        current_value, self.grid_data[i][j - 1]
                    ):
                        n.add_neighbour((i, j - 1))
                if j < max_cols - 1:
                    if self.check_letter(
                        current_value, self.grid_data[i][j + 1]
                    ):
                        n.add_neighbour((i, j + 1))
                if i > 0:
                    if self.check_letter(
                        current_value, self.grid_data[i - 1][j]
                    ):
                        n.add_neighbour((i - 1, j))
                if i < max_rows - 1:
                    if self.check_letter(
                        current_value, self.grid_data[i + 1][j]
                    ):
                        n.add_neighbour((i + 1, j))
                to_app.append(n)

            to_ret.append(to_app)
        return to_ret

    def get_next_value(self):
        vals = list(
            zip(self.tentative_values.values(), self.tentative_values.keys())
        )
        vals = list(filter(lambda x: x[0] is not None and x[1] in self.unchecked, vals))
        vals.sort()
        return vals[0][1]

    def run_iteration(self):
        i, j = self.current_value
        current_node = self.grid[i][j]
        for neigh in current_node.neighbours:
            if self.tentative_values[neigh] is None:

                self.tentative_values[neigh] = (
                    self.tentative_values[self.current_value] + 1
                )
            else:
                self.tentative_values[neigh] = min(
                    self.tentative_values[neigh],
                    self.tentative_values[self.current_value] + 1,
                )
        self.current_value = self.get_next_value()
        self.unchecked.remove(self.current_value)

    def __str__(self):
        rows = ["".join(x) for x in self.grid_data]
        return "\n".join(rows)


if __name__ == "__main__":
    start_time = dt.datetime.now().timestamp()
    print(start_time)
    data = get_data()
    grid = Grid(data=data)

    while grid.current_value != grid.end_point:
        grid.run_iteration()
    print(grid.tentative_values[grid.end_point])
    end_time = dt.datetime.now().timestamp()
    print(end_time - start_time)
