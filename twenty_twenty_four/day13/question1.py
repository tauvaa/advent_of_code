import os
import re

import numpy as np


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [line.strip() for line in f]
    to_ret = []
    to_app = []
    for d in data:
        if d == "" and to_app:
            to_ret.append(to_app)
            to_app = []
        else:
            to_app.append(d)
    if to_app:
        to_ret.append(to_app)

    return to_ret


def unpack_button(instring):
    to_ret = instring.split(":")[1].strip()
    to_ret = to_ret.split(",")
    to_ret = [int(x.split("+")[1]) for x in to_ret]
    return to_ret


def unpack_prize(instring):
    pattern = r"Prize: X=(\d+), Y=(\d+)"
    to_ret = re.findall(pattern, instring)

    return to_ret[0]


def read_data(data):
    button_a, button_b, prize = data
    button_a = unpack_button(button_a)
    button_b = unpack_button(button_b)
    prize = unpack_prize(prize)
    return button_a, button_b, prize


class Game:
    def __init__(self, button_a, button_b, prize):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize
        self.solution = None

    def solve_equation(self):
        button_a = np.array(self.button_a)
        button_b = np.array(self.button_b)
        prize = np.array(self.prize).astype(float)
        prize.shape = (2,1)
        mat = np.array([button_a, button_b]).transpose()
        imat = np.linalg.inv(mat)
        s = imat @ prize
        self.solution = s
    def get_solution(self):
        if self.solution is None:
            self.solve_equation()
        return self.solution

    def check_int_solution(self):
        # print(self.solution, self.prize)
        if self.solution is None:
            raise RuntimeError("solution not set")
        for v in self.solution:
            v = v[0]
            if v < 0:
                return False
            if abs(round(v) - v) > 1e-5:
                return False
        print(self.solution)
        return True
    def calculate_tokens(self):
        assert self.solution is not None
        a_clicks = self.solution[0,0]
        b_clicks = self.solution[1,0]
        a_clicks = round(a_clicks)
        b_clicks = round(b_clicks)
        return a_clicks * 3 + b_clicks

    


if __name__ == "__main__":
    data = get_data()
    total = 0
    counter = 0
    for d in data: 
        counter +=1
        d = read_data(d)
        g = Game(*d)
        g.solve_equation()
        if g.check_int_solution():
            total += g.calculate_tokens()
        # print(g.button_a, g.button_b, g.prize)
    print(total)



