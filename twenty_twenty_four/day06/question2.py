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
        self.in_loop = False
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

    def move(self):
        if self.guard_orientation == "up":
            next_blocks = [
                x
                for x in self.blocking_points
                if x[0] < self.guard_position[0] and x[1] == self.guard_position[1]
            ]
            # print(next_blocks)
            if len(next_blocks) == 0:
                # print("up")
                self.in_loop = False
                return False
            next_block = [
                x
                for x in next_blocks
                if x[0] == max([b[0] for b in next_blocks])
            ].pop()
            self.guard_position = (next_block[0] + 1, next_block[1])
            # print(self.guard_position)
            # print(next_block)

        if self.guard_orientation == "right":
            next_blocks = [
                x
                for x in self.blocking_points
                if x[0] == self.guard_position[0] and x[1] > self.guard_position[1]
            ]
            if len(next_blocks) == 0:
                self.in_loop = False
                # print("right")
                return False
            next_block = [
                x
                for x in next_blocks
                if x[1] == min([b[1] for b in next_blocks])
            ].pop()
            self.guard_position = (next_block[0], next_block[1] - 1)

        if self.guard_orientation == "down":
            next_blocks = [
                x
                for x in self.blocking_points
                if x[0] > self.guard_position[0] and x[1] == self.guard_position[1]
            ]
            if len(next_blocks) == 0:
                self.in_loop = False
                # print("down")
                return False
            next_block = [
                x
                for x in next_blocks
                if x[0] == min([b[0] for b in next_blocks])
            ].pop()
            self.guard_position = (next_block[0] - 1, next_block[1])

        if self.guard_orientation == "left":
            next_blocks = [
                x
                for x in self.blocking_points
                if x[0] == self.guard_position[0] and x[1] < self.guard_position[1]
            ]
            if len(next_blocks) == 0:
                self.in_loop = False
                # print("left")
                return False
            next_block = [
                x
                for x in next_blocks
                if x[1] == max([b[1] for b in next_blocks])
            ].pop()
            self.guard_position = (next_block[0], next_block[1] + 1)

        if (self.guard_position, self.guard_orientation) in self.places_visited:
            self.in_loop = True
            return False
        self.places_visited.add((self.guard_position, self.guard_orientation))
        self.turn_right()
        return True

        self.places_visited.add((self.guard_position, self.guard_orientation))

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
            if (self.guard_position, self.guard_orientation) in self.places_visited:
                self.in_loop = True
                return False
            self.places_visited.add((self.guard_position, self.guard_orientation))
        if self.get_map_point(next_position) == "#":
            self.turn_right()
        return True

    def turn_right(self):
        all_orientations = ["up", "right", "down", "left"]
        self.guard_orientation = all_orientations[
            (all_orientations.index(self.guard_orientation) + 1) % 4
        ]


if __name__ == "__main__":
    data = get_data()
    counter = 0
    total = len(data) * len(data[0])
    num_ran = 0
    for i, j in [(i, j) for i in range(len(data)) for j in range(len(data[0]))]:
        num_ran += 1
        if data[i][j] == ".":
            new_data = get_data()
            new_data[i][j] = "#"

            l = Layout(new_data)
            while l.move():
                pass
            # print(l.places_visited, "here", num_ran)
            if l.in_loop:
                counter += 1
        if num_ran % 100 == 0:
            print(num_ran, num_ran / total)
    print(counter)
