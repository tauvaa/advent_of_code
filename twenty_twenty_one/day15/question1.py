import os
import queue


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [[int(x) for x in list(line.strip())] for line in f]
    return data


class Grid:
    def __init__(self, data) -> None:
        self.data = data
        self.max_rows = len(data)
        self.max_cols = len(data[0])
        self.start_point = (0, 0)
        self.end_point = (self.max_rows - 1, self.max_cols - 1)

    def get_check_points(self, point):
        i, j = point
        to_ret = []
        if 0 <= i - 1:
            to_ret.append((i - 1, j))
        if i + 1 < self.max_rows:
            to_ret.append((i + 1, j))
        if 0 <= j - 1:
            to_ret.append((i, j - 1))
        if j + 1 < self.max_cols:
            to_ret.append((i, j + 1))
        return to_ret

    def get_point_value(self, point):
        i, j = point
        return self.data[i][j]

    def find_path(self):
        visited_points = set()
        qu = queue.PriorityQueue()

        current_point = None
        qu.put([0, self.start_point])
        print("checking: ", current_point)
        while current_point != self.end_point and not qu.empty():
            current = qu.get()
            current_point = current[1]
            if current_point in visited_points:
                continue
            print("checking: ", current_point)
            current_value = current[0]
            for p in self.get_check_points(current_point):
                if p not in visited_points:
                    point_val = self.get_point_value(p)
                    point_val += current_value

                    qu.put([point_val, p])
            visited_points.add(current_point)
        print(current)


if __name__ == "__main__":
    data = get_data()

    grid = Grid(data)
    grid.find_path()
