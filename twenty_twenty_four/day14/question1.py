import os
import re
import time
from functools import reduce


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [l.strip() for l in f if l.strip()]
    return data


def clean_data(data):
    reg_string = r"p=(.*),(.*) v=(.*),(.*)"
    to_ret = [[int(k) for k in re.findall(reg_string, d)[0]] for d in data]
    return to_ret


class Robot:
    def __init__(self, position, velocity) -> None:
        self.position = position
        self.velocity = velocity
        self.grid_x_size = 101
        self.grid_y_size = 103

    def take_step_n_steps(self, n=1):
        self.position = [
            (self.position[0] + self.velocity[0] * n) % self.grid_x_size,
            (self.position[1] + self.velocity[1] * n) % self.grid_y_size,
        ]


class Grid:
    def __init__(self, robots) -> None:
        self.grid_x_size = 101
        self.grid_y_size = 103
        self.robots = robots

    def move_robots(self, nsteps):
        for r in self.robots:
            r.take_step_n_steps(nsteps)

    def calculate_quadrents(self):
        quadrents = {1: 0, 2: 0, 3: 0, 4: 0}
        x_quadrent = int(self.grid_x_size / 2)
        y_quadrent = int(self.grid_y_size / 2)

        for r in self.robots:
            x_pos, y_pos = r.position
            if x_pos == x_quadrent or y_pos == y_quadrent:
                continue
            if x_pos < x_quadrent and y_pos < y_quadrent:
                quadrents[1] += 1
            elif x_pos > x_quadrent and y_pos < y_quadrent:
                quadrents[2] += 1
            elif x_pos < x_quadrent and y_pos > y_quadrent:
                quadrents[3] += 1
            elif x_pos > x_quadrent and y_pos > y_quadrent:
                quadrents[4] += 1
        return quadrents

    def check_tree(self):
        grid = ["." for _ in range(self.grid_x_size)]
        grid = [grid.copy() for _ in range(self.grid_y_size)]
        for r in robots:
            xp, yp = r.position
            grid[yp][xp] = "x"
        counter = 0
        for i, r in enumerate(grid):
            # print(i, r.count("x"))
            if 2 * i - 3 < r.count("x") < 2 * i + 3:
                counter += 1
        # print(counter)
        return counter > 50

    def __str__(self):
        grid = ["." for _ in range(self.grid_x_size)]
        grid = [grid.copy() for _ in range(self.grid_y_size)]
        for r in robots:
            xp, yp = r.position
            grid[yp][xp] = "x"
        grid = ["".join(g) for g in grid]
        return "\n".join(grid)


if __name__ == "__main__":
    data = get_data()
    data = clean_data(data)
    # print(data)
    robots = []
    for d in data:
        pos = [d[0], d[1]]
        vel = [d[2], d[3]]
        r = Robot(pos, vel)
        robots.append(r)
    g = Grid(robots)
    g.move_robots(100)
    quardtents = g.calculate_quadrents()
    quadrents = list(quardtents.values())

    safty_factor = reduce(lambda x, y: x * y, quadrents, 1)
    print(safty_factor)
