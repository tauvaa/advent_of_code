import json
import os


def get_data():
    to_ret = []
    to_app = []
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        for line in f:
            if line == "\n":
                to_ret.append(to_app)
                to_app = []

            else:
                to_app.append(json.loads(line.strip()))
        to_ret.append(to_app)
    return to_ret


def compare(left, right):
    for i, v in enumerate(left):
        if i > len(right) - 1:
            return False
        right_value = right[i]
        if all(isinstance(x, int) for x in (v, right_value)):
            if v < right_value:
                return True
            if v > right_value:
                return False
        elif isinstance(right_value, int) and isinstance(v, list):
            ret = compare(v, [right_value])
            if ret is not None:
                return ret

        elif isinstance(v, int) and isinstance(right_value, list):
            ret = compare([v], right_value)
            if ret is not None:
                return ret
        else:
            ret = compare(v, right_value)
            if ret is not None:
                return ret
    if len(right) > len(left):
        return True


class Signal:
    def __init__(self, signal, is_div=False):
        self.signal = signal
        self.is_div = is_div

    def __lt__(self, x):
        return compare(self.signal, x.signal)

    def __gt__(self, x):
        return not compare(self.signal, x.signal)


if __name__ == "__main__":

    all_points = [Signal([[2]], True), Signal([[6]], True)]
    data = get_data()
    for d in data:
        left, right = d

        all_points.append(Signal(left))
        all_points.append(Signal(right))
    all_points.sort()
    divs = 1
    for i, a in enumerate(all_points):
        print(a.signal)

        if a.is_div:
            divs *= i + 1
    print(divs)
    # for i, d in enumerate(data):
    #     left, right = d
    #     if compare(left=left, right=right):
    #         counter += i + 1
    # print(counter)
