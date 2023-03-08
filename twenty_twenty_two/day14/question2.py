import os
from functools import reduce


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [l.strip() for l in f]
    data = [x.split(" -> ") for x in data]
    data = [[list(map(int, cord.split(","))) for cord in elm] for elm in data]
    return data


def fill_rocks(rocks):
    to_ret = []
    for i in range(len(rocks) - 1):
        current_rock = rocks[i]
        next_rock = rocks[i + 1]
        if current_rock[0] != next_rock[0]:
            if current_rock[0] > next_rock[0]:
                for r in range(next_rock[0], current_rock[0]):
                    to_ret.append([r, current_rock[1]])
            else:
                for r in range(current_rock[0], next_rock[0]):
                    to_ret.append([r, current_rock[1]])

        elif current_rock[1] != next_rock[1]:
            if current_rock[1] > next_rock[1]:
                for r in range(next_rock[1], current_rock[1]):
                    print(r)
                    to_ret.append([current_rock[0], r])
            else:
                for r in range(current_rock[1], next_rock[1]):
                    print(r)
                    to_ret.append([current_rock[0], r])
    to_ret += rocks
    to_ret = [tuple(x) for x in to_ret]
    to_ret = list(set(to_ret))
    return to_ret


class Grid:
    def __init__(self, offset):
        # grid = ["." for _ in range(10)]

        self.grid = [["." for _ in range(40)] for _ in range(40)]
        self.rocks = []
        self.sand = []
        self.past_last_rock = False
        self.offset = offset
        self.max_depth = None
        self.sand_counter = 0

    def offset_point(self, point):
        x, y = point

        return (x - self.offset, y)

    def get_fixed_points(self):
        return set(self.rocks + self.sand)

    def get_max_rock_depth(self):
        self.max_depth = max([x[1] for x in rocks])

    def add_rock(self, rock):
        x, y = self.offset_point(rock)
        self.rocks.append(rock)
        # self.grid[y][x] = "#"

    def add_sand(self):
        for s in self.sand:
            offs = self.offset_point(s)
            x, y = offs
            self.grid[y][x] = "o"

    def drop_sand(self, current_point=(500, 0)):
        if current_point[1] == self.max_depth + 1:
            self.sand.append(current_point)
            self.sand_counter += 1 
            print("bottom: ", current_point, self.sand_counter)
        elif (
            current_point[0],
            current_point[1] + 1,
        ) not in self.get_fixed_points():
            current_point = (current_point[0], current_point[1] + 1)
            self.drop_sand(current_point=current_point)
        elif (
            current_point[0] - 1,
            current_point[1] + 1,
        ) not in self.get_fixed_points():
            current_point = (current_point[0] - 1, current_point[1] + 1)
            self.drop_sand(current_point)
        elif (
            current_point[0] + 1,
            current_point[1] + 1,
        ) not in self.get_fixed_points():
            current_point = (current_point[0] + 1, current_point[1] + 1)
            self.drop_sand(current_point)
        else:
            self.sand.append(current_point)
            self.sand_counter += 1
            print(current_point, self.sand_counter)
            if current_point[1] == 0:
                self.past_last_rock = True
                return

    def __str__(self):
        rows = ["".join(r) for r in self.grid]
        return "\n".join(rows)


if __name__ == "__main__":
    data = get_data()
    min_val = None
    for d in data:
        mind = min([x[0] for x in d])
        if min_val is None:
            min_val = mind
        min_val = min(min_val, mind)
    min_val -= 15
    print(min_val)
    rocks = list(map(fill_rocks, data))

    rocks = reduce(lambda x, y: x + y, rocks)

    grid = Grid(offset=min_val)
    for r in rocks:
        grid.add_rock(r)
    grid.get_max_rock_depth()
    grid.drop_sand()
    while not grid.past_last_rock:
        grid.drop_sand()

    # grid.add_sand()
    # print(grid)
    print(len(grid.sand))
    # print(grid.sand)
