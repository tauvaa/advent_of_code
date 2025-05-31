import os
from typing import Set, Tuple


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [line.strip() for line in f]
    data = [list(x) for x in data]
    return data


class Grid:
    def __init__(self, data) -> None:
        self.data = data
        self.num_rows = len(data)
        self.num_cols = len(data[0])
        self.all_points = [
            (i, j) for i in range(self.num_rows) for j in range(self.num_cols)
        ]

    def get_grid_point(self, row, col):
        if (0 <= row < self.num_rows) and (0 <= col < self.num_cols):
            return self.data[row][col]
        return None

    def check_left(self, row, col):
        return self.get_grid_point(row, col - 1), (row, col - 1)

    def check_right(self, row, col):
        return self.get_grid_point(row, col + 1), (row, col + 1)

    def check_up(self, row, col):
        return self.get_grid_point(row - 1, col), (row - 1, col)

    def check_down(self, row, col):
        return self.get_grid_point(row + 1, col), (row + 1, col)


class GridCalcuations(Grid):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.sections_points = set()
        self.visited_points = set()
        self.current_section = ""

    def _get_section(self, current_point):
        row, col = current_point
        self.sections_points.add(current_point)
        self.visited_points.add(current_point)
        section_name = self.get_grid_point(row, col)
        self.current_section = section_name
        for direction in (
            self.check_left(row, col),
            self.check_right(row, col),
            self.check_up(row, col),
            self.check_down(row, col),
        ):
            if (
                direction[0] == section_name
                and direction[1] not in self.sections_points
            ):
                self._get_section(direction[1])

    def clean_up(self):
        # self.visited_points = set()
        self.sections_points = set()
        self.current_section = ""

    def get_section(self, start_point):
        self.clean_up()
        self._get_section(start_point)

        return self.sections_points, self.current_section


def get_row_col_extreams(points: Set[Tuple]):
    max_row, min_row = None, None
    max_col, min_col = None, None
    for row, col in points:
        if max_row is None:
            max_row = row
        if min_row is None:
            min_row = row
        if max_col is None:
            max_col = col
        if min_col is None:
            min_col = col
        max_row = max(row, max_row)
        min_row = min(row, min_row)
        max_col = max(col, max_col)
        min_col = min(col, min_col)
    assert isinstance(max_col, int) and isinstance(max_row, int)
    return (min_row, max_row + 1), (min_col, max_col + 1)


def get_all_possible_corners(extreams):
    row_extreams, col_extreams = extreams
    row_min, row_max = row_extreams
    col_min, col_max = col_extreams
    return [
        (i, j) for i in range(row_min, row_max + 1) for j in range(col_min, col_max + 1)
    ]


def corner_order(corner, points):
    touch_blocks = []
    for offset in [(-1, -1), (-1, 0), (0, -1), (0, 0)]:
        if (corner[0] + offset[0], corner[1] + offset[1]) in points:
            touch_blocks.append(offset)
    if len(touch_blocks) % 2 == 1:
        return 1
    elif len(touch_blocks) == 2:
        o1, o2 = touch_blocks
        if o1[0] + o2[0] == o1[1] + o2[1] == -1:
            return 2
    return 0


def corner_counter(points):
    all_corners = get_all_possible_corners(get_row_col_extreams(points))
    total = 0
    for c in all_corners:
        total += corner_order(c, points)
    return total


if __name__ == "__main__":
    data = get_data()
    grid = GridCalcuations(data)
    total = 0
    for i, j in grid.all_points:
        if (i, j) not in grid.visited_points:
            g = grid.get_section((i, j))
            points, section = g
            total_corners = corner_counter(points)
            # print(section, len(points), total_corners, total_corners * len(points))
            total += total_corners * len(points)
    print(total)
