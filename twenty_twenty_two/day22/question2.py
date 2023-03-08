import os
from typing import Tuple


def get_data():
    grid = []
    grid_finished = False
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
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
        cube = Cube(50)
        return cube.wrap_point(point, self.facing)

    def take_step(self):
        if self.facing == "right":
            x, y = self.current_point

            new_point = (x, y + 1)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point, facing = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point
                    self.facing = facing

        elif self.facing == "left":
            x, y = self.current_point

            new_point = (x, y - 1)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point, facing = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point
                    self.facing = facing

        elif self.facing == "down":
            x, y = self.current_point

            new_point = (x + 1, y)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point, facing = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point
                    self.facing = facing

        elif self.facing == "up":
            x, y = self.current_point

            new_point = (x - 1, y)
            if new_point in self.walk_points:
                self.current_point = new_point
            elif new_point not in self.walls:
                wrap_point, facing = self.wrap_point(self.current_point)
                if wrap_point in self.walk_points:
                    self.current_point = wrap_point
                    self.facing = facing

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


class Cube:
    def __init__(self, cube_size) -> None:
        self.cube_size = cube_size
        self.grid = [
            ["_" for _ in range(self.cube_size * 4)]
            for _ in range(3 * self.cube_size)
        ]
        self.one_cord = self.make_face((0, 2))
        self.two_cord = self.make_face((1, 0))
        self.three_cord = self.make_face((1, 1))
        self.four_cord = self.make_face((1, 2))
        self.five_cord = self.make_face((2, 2))
        self.six_cord = self.make_face((2, 3))

    def make_face(self, grid_cord):
        xoffset, yoffset = grid_cord
        xoffset, yoffset = xoffset * self.cube_size, yoffset * self.cube_size
        all_cords = [
            (x + xoffset, y + yoffset)
            for x in range(self.cube_size)
            for y in range(self.cube_size)
        ]
        return all_cords

    def __str__(self):
        grid = self.grid.copy()
        for c in self.one_cord:
            x, y = c
            grid[x][y] = "1"

        for c in self.two_cord:
            x, y = c
            grid[x][y] = "2"

        for c in self.three_cord:
            x, y = c
            grid[x][y] = "3"

        for c in self.four_cord:
            x, y = c
            grid[x][y] = "4"
        for c in self.five_cord:
            x, y = c
            grid[x][y] = "5"
        for c in self.six_cord:
            x, y = c
            grid[x][y] = "6"

        rows = ["".join(r) for r in grid]
        return "\n".join(rows)

    def wrap_point(self, point, facing):
        x, y = point
        if point in self.one_cord:
            if facing == "up":
                x_offset = self.cube_size
                y_offset = -self.cube_size * 2
                y_point = y + y_offset
                y_point = self.cube_size - y_point - 1
                return (x + x_offset, y_point), "down"
            elif facing == "right":
                x_offset = self.cube_size * 2
                y_offset = self.cube_size * 4
                return ((x + x_offset, y_offset - 1), "left")
            elif facing == "left":
                x_point = self.cube_size
                y_point = self.cube_size + x

                return (x_point, y_point), "down"

        elif point in self.two_cord:
            if facing == "up":
                x_offset = 0
                y_offset = self.cube_size * 2
                y_point = y_offset + self.cube_size - y - 1
                return (x + x_offset, y_point), "down"
            elif facing == "down":
                x_offset = self.cube_size * 3 - 1
                y_offset = self.cube_size * 2
                y_point = y_offset + (self.cube_size - y - 1)
                return ((x_offset, y_point), "up")
            elif facing == "left":
                y_point = 3 * self.cube_size - 1

                return (x, y_point), "left"

        elif point in self.three_cord:
            if facing == "down":
                y_point = 2 * self.cube_size
                x_point = y - self.cube_size
                x_point = self.cube_size - 1 - x_point
                x_point = x_point + self.cube_size * 2

                return (x_point, y_point), "right"
            elif facing == "up":
                y_point = 2 * self.cube_size
                x_offset = self.cube_size
                x_point = y - x_offset
                return ((x_point, y_point), "right")

        elif point in self.four_cord:
            if facing == "right":
                x_point = self.cube_size * 2
                y_point = x - self.cube_size
                y_point = self.cube_size * 3 + (self.cube_size - 1 - y_point)
                return (x_point, y_point), "down"

        elif point in self.five_cord:
            if facing == "left":
                x_point = self.cube_size * 2 - 1
                y_point = x - self.cube_size * 2
                y_point = self.cube_size + (self.cube_size - 1 - y_point)
                return (x_point, y_point), "up"
            if facing == "down":
                x_point = self.cube_size * 2 - 1
                y_point = y - self.cube_size * 2
                y_point = self.cube_size - 1 - y_point
                return (x_point, y_point), "up"
        elif point in self.six_cord:
            if facing == "up":
                y_point = self.cube_size * 3 - 1
                x_point = y - 3 * self.cube_size
                x_point = self.cube_size * 2 - 1 - x_point
                return (x_point, y_point), "left"

            if facing == "down":
                x_point = self.cube_size * 2 - 1
                y_point = y - self.cube_size * 3
                y_point = self.cube_size - 1 - y_point
                return (x_point, y_point), "up"

            if facing == "right":
                y_point = self.cube_size * 3 - 1
                x_point = x - self.cube_size * 2
                x_point = self.cube_size - 1 - x_point
                return (x_point, y_point), "left"


if __name__ == "__main__":
    cube = Cube(50)
    print(cube)
    exit()
    grid, instructions = get_data()
    print(max(map(len, grid)))
    grid = Grid(grid)
    print(grid)
    instructions = parse_instructions(instructions)
    for inst in instructions:
        if isinstance(inst, int):
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
