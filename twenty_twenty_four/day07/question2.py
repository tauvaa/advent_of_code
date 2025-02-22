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
    def evaluate_equation(self, opstring):
        numbers = self.eq_string.split(" ")
        numbers = list(map(int, numbers))
        current_num = numbers.pop(0)
        for i, num in enumerate(numbers):
            op = opstring[i]
            if op == "*":
                current_num *=num
            if op == "+":
                current_num += num
            if op == "c":
                current_num = current_num * 10**len(str(num)) + num
        return current_num

                
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
        new_ops.append(s + "c")
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
                if equation.answer == equation.evaluate_equation(opstring):
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
