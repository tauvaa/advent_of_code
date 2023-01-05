"""Question 1."""
import datetime as dt
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
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [line.strip() for line in f]
    data = list(data[0])
    return data


class Timer:
    def __init__(self) -> None:
        self.start_time = dt.datetime.now().timestamp()
        self.time_dict = {}

    def get_time_diff(self):
        return dt.datetime.now().timestamp() - self.start_time

    def add_time(self, label):
        if label not in self.time_dict:
            self.time_dict[label] = 0
        self.time_dict[label] += self.get_time_diff()


class Grid:
    def __init__(self, instructions) -> None:
        self.grid = [list(["." for _ in range(30)]) for _ in range(30)]
        self.instructions = instructions
        self.rock = None
        self.stopped_rocks = []
        self.highest_rock = 0
        self.timer = Timer()
        self.rocks = {}
        self.keep_last = 50
        self.to_keep = []

    def keep_vals(self, rock):
        check_val = self.highest_rock - self.keep_last
        for r in rock:
            if r[0] > check_val:
                self.to_keep.append(r)
        self.to_keep = list(filter(lambda x: x[0] >= check_val, self.to_keep))
        self.to_keep.sort()

    def get_keep_vals(self):
        to_ret = self.to_keep.copy()
        to_shift = self.highest_rock - self.keep_last

        to_ret = [(x[0] - to_shift, x[1]) for x in to_ret]
        return str(to_ret)

    def reset_grid(self):
        self.grid = [list(["." for _ in range(30)]) for _ in range(30)]

    def check_cycle(self):
        return [x[1] for x in self.rocks if x[0] == self.highest_rock]

    def get_highest(self):
        old_highest = self.highest_rock
        self.highest_rock = max([x[0] for x in self.rocks])

    def add_rocks(self):

        for r in self.rock:
            self.rocks[r] = 1

    def move_rock(self, instruction):
        if instruction == ">":
            # print("right")
            mover = 1
        if instruction == "<":
            # print("left")
            mover = -1
        rock_cols = [x[1] for x in self.rock]
        if not (0 <= min(rock_cols) + mover and max(rock_cols) + mover < 7):
            mover = 0

        new_rock = list(map(lambda x: (x[0], x[1] + mover), self.rock))
        if any(x in self.rocks for x in new_rock):
            new_rock = self.rock
        self.rock = new_rock
        new_rock = list(map(lambda x: (x[0] - 1, x[1]), self.rock))
        if any(x in self.rocks for x in new_rock):

            self.add_rocks()
            old_rock = self.rock

            self.rock = None
            self.get_highest()
            self.keep_vals(old_rock)
            return

        self.rock = new_rock

        if min([x[0] for x in self.rock]) == 0:
            self.add_rocks()
            old_rock = self.rock
            self.rock = None
            self.get_highest()
            self.keep_vals(old_rock)

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
        for rock in self.rocks:
            i, j = rock
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
    cycles = {i: [] for i in range(4)}
    cycle_counter = 0
    cycle_size = 0
    target = 1000_000_000_000
    while counter < target:
        rock = rocks[counter % len(rocks)]
        rock = get_rock_cordinate(rock)

        grid.add_rock(rock)

        while grid.rock:
            instruct = data[instruct_counter % len(data)]
            starttime = dt.datetime.now().timestamp()
            grid.move_rock(instruct)
            endtime = dt.datetime.now().timestamp()
            # print("move took: ", endtime - starttime)
            instruct_counter += 1
        kv = grid.get_keep_vals()
        kv = str(instruct_counter % len(data)) + kv
        if kv in [x[0] for x in cycles[counter % 4]]:
            print("fount!!", counter)
            m = [x for x in cycles[counter % 4] if x[0] == kv]
            m = m[0][1:]
            print(m, grid.highest_rock, counter)
            gap = counter - m[0]
            height_gap = grid.highest_rock - m[1]

            print(f"gap {gap} height gap: {height_gap}")
            if (target - counter) % gap == 0:
                print(
                    int(height_gap * (target - counter) / gap)
                    + grid.highest_rock
                )
                print("test")
                exit()

            cycle_counter += 1
        if cycle_counter > 10:

            print("here")

            current_height = grid.highest_rock
        cycles[counter % 4].append((kv, counter, grid.highest_rock))

        print("starting instrcutions")
        # print("=" * 100)

        # grid.draw_rocks()
        counter += 1
        print(counter, "counter")
    print(cycles)
    print(grid.highest_rock + 1)
    print(min([x[0] for x in grid.to_keep]))
