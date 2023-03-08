import os
import bigfloat

from sympy import Eq, solve, symbols


class Operation:
    def __init__(self, opstring) -> None:
        self.opstring = opstring
        opstring = opstring.split(" ")
        self.left_name, self.operation, self.right_name = opstring

    def __str__(self):
        return f"""left: {self.left_name}, right: {self.right_name}, op: {self.operation}"""

    def run_op(self, left_value, right_value, varname):
        if varname == "root":
            return left_value == right_value
        if self.operation == "+":
            return left_value + right_value
        if self.operation == "-":
            return left_value - right_value
        if self.operation == "*":
            return left_value * right_value
        if self.operation == "/":
            return int(left_value / right_value)


def combine_vals(left, right, operation, data, to_ret=True, symb="x"):
    left = data[left]
    right = data[right]
    if len(left.split(" ")) > 1:
        tleft, op, tright = left.split()
        tleft = tleft.strip()
        op = op.strip()
        tright = tright.strip()
        left = combine_vals(tleft, tright, op, data, False)
    if len(right.split(" ")) > 1:
        tleft, op, tright = right.split()
        tleft = tleft.strip()
        op = op.strip()
        tright = tright.strip()
        right = combine_vals(tleft, tright, op, data, False)
    if to_ret:
        return left, right

    to_ret = f"({left} {operation} {right})"
    try:
        if symb not in to_ret:
            exec(f"m = {to_ret}", None, globals())
            return m
        return to_ret
    except Exception as e:
        raise e


def get_data(opdata=False):
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [l.strip() for l in f]
    to_ret = []
    if not opdata:
        for d in data:
            name, op = d.split(":")
            name = name.strip()

            op = op.strip()
            if len(op.split(" ")) > 1:
                op = Operation(op)
            else:
                op = int(op)

            to_ret.append((name, op))
    else:
        for d in data:
            name, op = d.split(":")
            name = name.strip()

            op = op.strip()
            to_ret.append((name, op))
    return to_ret


def breakdown_string(instring, symb="x"):
    ops = list("*/+-")
    instring = instring.strip(" ")
    instring = instring.strip(")").strip("(")
    to_ret = []
    for x in ops:
        if len(instring.split(x)) > 1:
            left, right = instring.split(x, 1)
            if "(" not in left and ")" not in left:
                if left.strip() == symb:
                    instring = "(" + instring
                else:

                    to_ret.append((x, left))
                    instring = right
            splitter = instring.split(x)
            if "(" not in splitter[-1] and ")" not in splitter[-1]:
                print("here")
                to_ret.append((x, splitter[-1]))
                instring = x.join(splitter[0:-1])

    if (
        len(to_ret) > 1
        and to_ret[1][0] in ("*", "/")
        and to_ret[0][0] not in ("*", "/")
    ):
        to_ret.reverse()
    return to_ret, instring


if __name__ == "__main__":

    data = get_data(True)
    data = {x[0]: x[1] for x in data}
    root = data["root"]
    root = Operation(root)
    data["humn"] = "x"
    left, right = combine_vals(
        root.left_name, root.right_name, root.operation, data
    )
    left1 = left
    a = right
    a = int(a)
    left = left + f" - {a}"
    x = symbols("x")
    e = eval(f"Eq({left})")
    s = solve((e,), (x,))
    print(s[x])

    def derivative(func, point):
        ofset = 10 ** -1
        print(func(point), func(point + ofset))

        return (func(point + ofset) - func(point)) / ofset

    fun = lambda x: eval(left)

    def newton_method(x, func):
        der = derivative(func, x)
        return x - func(x) / der

    inguess = newton_method(fun(100), fun)
    for i in range(100):
        inguess = newton_method(inguess, fun)
        print(inguess)
    # all_ops = []
    # print(left)
    # for i in range(1000):
    #     ops, left = breakdown_string(left)
    #     all_ops += ops
    #     print(left)
    # t = []
    # for o in all_ops:
    #     op, num = o
    #     print(op)
    #     if op == "+":
    #         new_op = "-"
    #     if op == "-":
    #         new_op = "+"
    #     if op == "*":
    #         new_op = "/"
    #     if op == "/":
    #         new_op = "*"
    #     t.append((new_op, int(float(num.strip()))))
    # num = int(right)
    # a = num
    # for x in t:
    #     todo = f"a={a} {x[0]} {x[1]}"
    #     print(todo)
    #     print(exec(todo))
    #     print(a)
    # x = a
    # exec(f"print('here', {left1})")
    # print(left1)
    # for x in range(-100000, 0):
    #     exec(f"b = {left}")
    #     if b == a:

    #         print("the value is: ", x)
    #         break
    #     if x % 1000 == 0:
    #         print(x)

    # for i in range(100000):
    #     num_dic = {}
    #     data = [d if d[0] != "humn" else (d[0], i) for d in data]
    #     missing_op = True
    #     while missing_op:
    #         missing_op = False
    #         for d in data:
    #             if isinstance(d[1], Operation):
    #                 if all(
    #                     x in num_dic for x in (d[1].left_name, d[1].right_name)
    #                 ):
    #                     l, r = num_dic[d[1].left_name], num_dic[d[1].right_name]
    #                     num_dic[d[0]] = d[1].run_op(l, r, d[0])
    #                     if d[0] == "root" and num_dic.get("root"):
    #                         break
    #                 else:
    #                     missing_op = True

    #             else:
    #                 num_dic[d[0]] = d[1]
    #     if num_dic["root"]:
    #         print("humn is: ", i)
    #         break
    #     print(i)
