"""Question 1."""
import os
from functools import reduce


def get_rock_shapes():
    """Used to get rock shapes."""
    with open(
        os.path.join(os.path.dirname(__file__), "data", "rockshapes")
    ) as f:
        rock_shapes = f.read()
    to_ret = []
    to_app = []
    for line in rock_shapes.split("\n"):
        if line == "":
            to_app.reverse()
            to_ret.append(to_app)
            to_app = []

        else:
            # line = list(line)
            # line.reverse()
            # line = "".join(line)
            to_app.append(line)

    return to_ret


def get_rock_cordinate(rock):

    """Use to get rock cordinates."""
    to_ret = []

    for i in range(len(rock)):
        for j in range(len(rock[0])):
            if rock[i][j] == "#":
                to_ret.append((i, j))
    return to_ret


def get_data():
    """Use to get data."""
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [line.strip() for line in f]
    data = list(data[0])
    return data


class Grid:
    def __init__(self, instructions) -> None:
        self.grid = [list(["." for _ in range(30)]) for _ in range(30)]
        self.instructions = instructions
        self.rock = None
        self.stopped_rocks = []
        self.highest_rock = 0

    def reset_grid(self):
        self.grid = [list(["." for _ in range(30)]) for _ in range(30)]

    def get_highest(self):
        self.highest_rock = max(
            [x[0] for x in reduce(lambda x, y: x + y, self.stopped_rocks)]
        )

    def move_rock(self, instruction):
        if instruction == ">":
            print("right")
            mover = 1
        if instruction == "<":
            print("left")
            mover = -1
        rock_cols = [x[1] for x in self.rock]
        if not (0 <= min(rock_cols) + mover and max(rock_cols) + mover < 7):
            mover = 0

        new_rock = list(map(lambda x: (x[0], x[1] + mover), self.rock))
        for ro in new_rock:
            for r in self.stopped_rocks:
                for k in r:
                    if ro == k:
                        print("changing rocks")
                        new_rock = self.rock
        self.rock = new_rock
        new_rock = list(map(lambda x: (x[0] - 1, x[1]), self.rock))
        for ro in new_rock:
            for r in self.stopped_rocks:
                for k in r:
                    if ro == k:
                        print("changing rocks")
                        self.stopped_rocks = [self.rock] + self.stopped_rocks

                        self.rock = None
                        self.get_highest()
                        return

        self.rock = new_rock

        if min([x[0] for x in self.rock]) == 0:
            self.stopped_rocks.append(self.rock)
            self.rock = None

    def add_rock(self, rock):
        offset = self.highest_rock + 4
        rock = list(map(lambda x: (x[0] + offset, x[1] + 2), rock))
        self.rock = rock

    def __str__(self) -> str:
        rows = ["".join(x) for x in self.grid]
        rows.reverse()
        return "\n".join([r for r in rows])

    def draw_rocks(self):
        self.reset_grid()
        if self.rock is not None:
            for x in self.rock:
                i, j = x
                self.grid[i][j] = "#"
        for rock in self.stopped_rocks:
            for x in rock:
                i, j = x
                self.grid[i][j] = "#"

    def run(self):
        print("hello world")


if __name__ == "__main__":
    data = get_data()
    counter = 0
    rocks = get_rock_shapes()
    grid = Grid(data)
    grid.add_rock(get_rock_cordinate(rocks[2]))
    grid.draw_rocks()
    instruct_counter = 0
    while counter < 2022:
        rock = rocks[counter % len(rocks)]
        rock = get_rock_cordinate(rock)

        grid.add_rock(rock)

        while grid.rock:
            instruct = data[instruct_counter % len(data)]
            grid.move_rock(instruct)
            instruct_counter += 1
            print("=" * 100)
            # grid.draw_rocks()
        counter += 1
        print(counter, "counter")
    print(grid.highest_rock + 1)
    # grid.draw_rocks()
    # print(grid)
