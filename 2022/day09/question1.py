import enum
import os
import random
import string

import numpy as np
import pandas as pd


class Instructions(enum.Enum):
    left = "L"
    right = "R"
    up = "U"
    down = "D"


def get_random_string(string_size):
    return "".join(
        [random.choice(list(string.ascii_letters)) for _ in range(string_size)]
    )


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f]

    return data


def make_data(indata):
    to_ret = []
    for a in indata:
        instruct, counter = a.split()
        instruct = Instructions(instruct)
        counter = int(counter)
        for _ in range(counter):
            to_ret.append(instruct)
    return to_ret


class Solution:
    def __init__(self):
        self.head_position = (0, 0)
        self.tail_position = (0, 0)
        self.tail_positions = []

    def take_step(self, instruction):
        """take a step instruction (right, left, up, down)"""
        if instruction == Instructions.down:
            self.move_down()
        elif instruction == Instructions.up:
            self.move_up()
        elif instruction == Instructions.right:
            self.move_right()
        elif instruction == Instructions.left:
            self.move_left()
        self.check_distance()

    def move_tail_left_right(self, distance):
        if distance[0] > 1:
            self.tail_position = (
                self.tail_position[0] + 1,
                self.tail_position[1],
            )
        elif distance[0] < -1:
            self.tail_position = (
                self.tail_position[0] - 1,
                self.tail_position[1],
            )
        if distance[1] > 1:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] + 1,
            )
        elif distance[1] < -1:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] - 1,
            )
        self.tail_positions.append(self.tail_position)

    def move_diagonal(self, distance):
        print("move diagonal")
        x, y = distance
        if x < 0:
            self.tail_position = (
                self.tail_position[0] - 1,
                self.tail_position[1],
            )
        if x > 0:
            self.tail_position = (
                self.tail_position[0] + 1,
                self.tail_position[1],
            )
        if y < 0:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] - 1,
            )
        if y > 0:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] + 1,
            )
        # print(self.head_position, self.tail_position)
        self.tail_positions.append(self.tail_position)

    def check_distance(self):
        distance = tuple(
            (self.head_position[i] - self.tail_position[i] for i in range(2))
        )
        print(distance)
        if sum(map(abs, distance)) == 3:
            self.move_diagonal(distance=distance)
        else:
            self.move_tail_left_right(distance=distance)

    def move_right(self):
        print("moved right")
        x, y = self.head_position
        self.head_position = (x, y + 1)

    def move_left(self):
        print("moved left")
        x, y = self.head_position
        self.head_position = (x, y - 1)

    def move_up(self):
        print("moved up")
        x, y = self.head_position
        self.head_position = (x + 1, y)

    def move_down(self):
        print("moved down")
        x, y = self.head_position
        self.head_position = (x - 1, y)


if __name__ == "__main__":
    data = get_data()
    instructions = make_data(data)
    solution = Solution()
    for instruction in instructions:
        solution.take_step(instruction)
    tp = solution.tail_positions
    tp = set(tp)
    print(len(tp))
