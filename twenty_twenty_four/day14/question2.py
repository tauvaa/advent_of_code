import os
import re
import time
from functools import reduce
from typing import List


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
    def get_loop(self):
        """
        max_iterations before robot is in same starting place
        """
        pos = self.position
        counter = 0
        self.take_step_n_steps(1)
        counter += 1
        while pos != self.position:
            self.take_step_n_steps(1)
            counter += 1
        return counter


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
        for r in self.robots:
            xp, yp = r.position
            grid[yp][xp] = "x"
        counter = 0
        for i, r in enumerate(grid):
            if i - 3 < r.count("x") < i + 3:
                counter += 1
        return counter > 50

    def __str__(self):
        grid = ["." for _ in range(self.grid_x_size)]
        grid = [grid.copy() for _ in range(self.grid_y_size)]
        for r in self.robots:
            xp, yp = r.position
            grid[yp][xp] = "x"
        grid = ["".join(g) for g in grid]
        return "\n".join(grid)


def make_tree_data():

    robots = []
    grid = Grid(robots=[])

    middle = int(grid.grid_x_size / 2)
    for i in range(int(grid.grid_y_size)):
        for k in range(int(i/2)):
            pos = [middle + k, i]
            robot = Robot(pos, [0, 0])
            robots.append(robot)

            pos = [middle - k, i]
            robot = Robot(pos, [0, 0])
            robots.append(robot)
    grid.robots = robots
    # grid = Grid(robots)
    print(grid.robots[-1].position)
    print(grid)
    print(grid.check_tree())


if __name__ == "__main__":

    data = get_data()

    data = clean_data(data)
    # print(data)
    robots:List[Robot] = []
    for d in data:
        pos = [d[0], d[1]]
        vel = [d[2], d[3]]
        r = Robot(pos, vel)
        robots.append(r)
    # make_tree_data()
    g = Grid(robots)
    msf = None
    msfi= None
    for i in range(10_403):
        if i % 1000 == 0:
            print(f"on iteration: {i}")
        quardtents = g.calculate_quadrents()
        quadrents = list(quardtents.values())
        safty_factor = reduce(lambda x, y: x * y, quadrents, 1)
        if msf is None:
            msf = safty_factor
        if msf > safty_factor:
            msfi = i
        msf = min(msf, safty_factor)

        g.move_robots(1)
    g.move_robots(7623)
    print(g)
    print(msf, msfi)

