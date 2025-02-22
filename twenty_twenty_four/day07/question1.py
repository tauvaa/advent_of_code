import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [l.strip() for l in f]
    return data


class Equation:
    def __init__(self, answer, eq_string):
        self.answer = int(answer)
        self.eq_string = eq_string.strip()
    def get_spaces(self):
        return len(re.findall(" ", self.eq_string))
    def make_eq_string(self, operations_string):
        to_ret = ""
        opindex = 0
        for c in self.eq_string:
            if c == " ":
                to_ret = f"({to_ret}){operations_string[opindex]}"
                opindex += 1
            else:
                to_ret += c
        return to_ret
                
    def __str__(self):
        return f"answer: {self.answer}\neq_string: {self.eq_string}"


def clean_data(dataline):
    answer, eq_string = dataline.split(":")
    return Equation(answer, eq_string)


def get_op_possibilities(num_ops, start_ops=[""], all_ops={}):
    new_ops = []
    for s in start_ops:
        new_ops.append(s + "+")
        new_ops.append(s + "*")
    all_ops[len(new_ops[0])] = new_ops
    if len(new_ops[0]) == num_ops:
        return new_ops
    return get_op_possibilities(num_ops, new_ops, all_ops=all_ops)


class Solution:
    def __init__(self, inputdata):
        self.data = inputdata
        self.all_ops = {}
    def solve(self):
        valid_equations = []
        for equation in data:
            num_ops = equation.get_spaces()
            if num_ops not in self.all_ops:
                get_op_possibilities(num_ops, all_ops=self.all_ops)
            opstrings = self.all_ops[num_ops]
            for opstring in opstrings:
                check_eq = equation.make_eq_string(opstring)
                if equation.answer == eval(check_eq):
                    valid_equations.append(equation)
                    break
        return valid_equations



if __name__ == "__main__":
    data = get_data()
    data = map(clean_data, data)

    solution = Solution(data)
    total = 0
    for s in solution.solve():
        total +=s.answer
    print(total)
