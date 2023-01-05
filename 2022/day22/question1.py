import os
from typing import Tuple


def get_data():
    grid = []
    grid_finished = False
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        for line in f:
            if line != "\n":
                if grid_finished:
                    instructions = line.strip()
                else:
                    grid.append(line.strip("\n"))

            else:
                grid_finished = True

    return grid, instructions


def parse_instructions(instructions):
    to_ret = []
    current = ""
    for i in instructions:
        if i not in ("R", "L"):
            current += i
        else:
            to_ret.append(int(current))
            to_ret.append(i)
            current = ""
    if current:
        to_ret.append(int(current))
    return to_ret

class Grid:
    def __init__(self, grid_data) -> None:
        self.walk_points = []
        self.walls = []
        self.make_grid(grid_data)
        self.current_point = self.initialize_point()
        self.facing = "right"
        self.all_points = [(self.current_point, self.facing)]

    def make_grid(self, grid_data):

        for i, r in enumerate(grid_data):
            for j, v in enumerate(r):
                if v == "#":
                    self.walls.append((i, j))
                elif v == ".":
                    self.walk_points.append((i, j))

    def turn(self, turn):
        if self.facing == "right" and turn == "L":
            self.facing = "up"
        elif self.facing == "right" and turn == "R":
            self.facing = "down"

        elif self.facing == "left" and turn == "L":
            self.facing = "down"
        elif self.facing == "left" and turn == "R":
            self.facing = "up"

        elif self.facing == "up" and turn == "L":
            self.facing = "left"
        elif self.facing == "up" and turn == "R":
            self.facing = "right"

        elif self.facing == "down" and turn == "L":
            self.facing = "right"
        elif self.facing == "down" and turn == "R":
            self.facing = "left"
        else:
            raise RuntimeError("not found")

    def initialize_point(self):
        all_points = list(
            filter(lambda x: x[0] == 0, self.walls + self.walk_points)
        )
        min_y = min([x[1] for x in all_points])
        return (0, min_y)

    def wrap_point(self, point):
        x, y = point
        if self.facing == "right":
            y_point = min(
                [k[1] for k in (self.walls + self.walk_points) if k[0] == x]
            )
            return (x, y_point)

        if self.facing == "left":
            y_point = max(
                [k[1] for k in (self.walls + self.walk_points) if k[0] == x]
            )
            return (x, y_point)

        if self.facing == "up":
            x_point = max(
                [k[0] for k in (self.walls + self.walk_points) if k[1] == y]
            )
            return (x_point, y)

        if self.facing == "down":
            x_point = min(
                [k[0] for k in (self.walls + self.walk_points) if k[1] == y]
            )
            return (x_point, y)

    def take_step(self):
        if self.facing == "right":
            x, y = self.current_point

            new_point = (x, y + 1)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point

        elif self.facing == "left":
            x, y = self.current_point

            new_point = (x, y - 1)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point

        elif self.facing == "down":
            x, y = self.current_point

            new_point = (x + 1, y)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point

        elif self.facing == "up":
            x, y = self.current_point

            new_point = (x - 1, y)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point

    def __str__(self):
        row_len = max([x[0] for x in self.walls + self.walk_points]) + 1
        col_len = max([x[1] for x in self.walls + self.walk_points]) + 1

        grid = [[" " for _ in range(col_len)] for _ in range(row_len)]
        for val in self.walk_points:
            grid[val[0]][val[1]] = "."
        for val in self.walls:
            grid[val[0]][val[1]] = "#"
        for val in self.all_points:
            v, f = val
            if f == "right":
                symb = ">"
            if f == "left":
                symb = "<"
            if f == "up":
                symb = "^"
            if f == "down":
                symb = "v"
            grid[v[0]][v[1]] = symb
        rows = ["".join(r) for r in grid]
        to_ret = "\n".join(rows)
        to_ret += "\n"
        to_ret += "=" * 100
        return to_ret


if __name__ == "__main__":
    grid, instructions = get_data()
    grid = Grid(grid)
    print(grid)
    instructions = parse_instructions(instructions)
    for inst in instructions:
        if isinstance(inst, int):
            print(inst)
            for _ in range(inst):
                grid.take_step()
        else:

            grid.turn(inst)
    point, face = grid.current_point, grid.facing
    point = (point[0] + 1, point[1] + 1)
    row, column = point
    print(face)
    face = "right down left up".split().index(face)
    print(face, row, column)
    print(1000 * row + 4 * column + face)
