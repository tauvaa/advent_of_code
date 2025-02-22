import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [list(x.strip()) for x in f]
    return data


class Layout:
    def __init__(self, init_layout):
        self.layout = init_layout
        self.num_rows = len(init_layout)
        self.num_cols = len(init_layout[0])
        self.blocking_points = []
        self.guard_position = None
        self.guard_orientation = None
        self.places_visited = set()
        self.max_rows = len(init_layout)
        self.max_cols = len(init_layout[0])
        self.get_points_init_points()

    def set_guard_orientation(self, point):
        char = self.layout[point[0]][point[1]]
        if char == "^":
            self.guard_orientation = "up"
        elif char == ">":
            self.guard_orientation = "right"
        elif char == "v":
            self.guard_orientation = "down"
        elif char == "<":
            self.guard_orientation = "left"

    def get_map_point(self, point):
        row, col = point
        return self.layout[row][col]

    def get_points_init_points(self):
        for i, j in [
            (i, j) for i in range(self.num_rows) for j in range(self.num_cols)
        ]:
            if self.layout[i][j] == "#":
                self.blocking_points.append((i, j))
            elif self.layout[i][j] in ("^", ">", "v", "<"):
                self.guard_position = (i, j)
                self.set_guard_orientation(self.guard_position)

    def __str__(self):
        to_ret = "\n".join(["".join(x) for x in self.layout])
        return to_ret

    def take_step(self):
        if self.guard_orientation == "up":
            next_position = (self.guard_position[0] - 1, self.guard_position[1])
            guard_symbol = "^"
        elif self.guard_orientation == "right":
            next_position = (self.guard_position[0], self.guard_position[1] + 1)
            guard_symbol = ">"
        elif self.guard_orientation == "down":
            next_position = (self.guard_position[0] + 1, self.guard_position[1])
            guard_symbol = "v"
        elif self.guard_orientation == "left":
            next_position = (self.guard_position[0], self.guard_position[1] - 1)
            guard_symbol = "<"
        if (
            0 > next_position[0]
            or 0 > next_position[1]
            or next_position[0] >= self.max_rows
            or next_position[1] >= self.max_cols
        ):
            return False

        if self.get_map_point(next_position) == ".":
            self.layout[self.guard_position[0]][self.guard_position[1]] = "."
            self.layout[next_position[0]][next_position[1]] = guard_symbol
            self.guard_position = next_position
            self.places_visited.add(self.guard_position)
        if self.get_map_point(next_position) == "#":
            self.turn_right()
        return True

    def turn_right(self):
        all_orientations = ["up", "right", "down", "left"]
        self.guard_orientation = all_orientations[
            (all_orientations.index(self.guard_orientation) + 1) % 4
        ]


if __name__ == "__main__":
    l = Layout(get_data())
    while l.take_step():
        pass
    print(len(l.places_visited))
