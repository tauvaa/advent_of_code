import os


class Operation:
    def __init__(self, opstring) -> None:
        opstring = opstring.split(" ")
        self.left_name, self.operation, self.right_name = opstring

    def __str__(self):
        return f"""left {self.left_name}, right: {self.right_name}, op: {self.operation}"""

    def run_op(self, left_value, right_value):
        if self.operation == "+":
            return left_value + right_value
        if self.operation == "-":
            return left_value - right_value
        if self.operation == "*":
            return left_value * right_value
        if self.operation == "/":
            return int(left_value / right_value)


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [l.strip() for l in f]
    to_ret = []
    for d in data:
        name, op = d.split(":")
        name = name.strip()

        op = op.strip()
        if len(op.split(" ")) > 1:
            op = Operation(op)
        else:
            op = int(op)

        to_ret.append((name, op))
    return to_ret


if __name__ == "__main__":
    num_dic = {}

    data = get_data()
    missing_op = True
    while missing_op:
        missing_op = False
        for d in data:
            if isinstance(d[1], Operation):
                if all(x in num_dic for x in (d[1].left_name, d[1].right_name)):
                    l, r = num_dic[d[1].left_name], num_dic[d[1].right_name]
                    num_dic[d[0]] = d[1].run_op(l, r)
                else:
                    missing_op = True
                    print(d[1].left_name, d[1].right_name)
                    print(num_dic)

            else:
                num_dic[d[0]] = d[1]
    print(num_dic)
