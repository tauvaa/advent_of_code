import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f]
    return data


class Chuncker:
    def __init__(self, data) -> None:
        self.data = data
        self.open_chars = list("([{<")
        self.close_chars = list(")]}>")
        self.close_char_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self.expected_closers = []
        self.index = 0
        self.has_more = True

    def move_string(self):
        current_char = self.data[self.index]
        if current_char in self.close_chars:
            next_close = self.expected_closers.pop(-1)
            if next_close != current_char:
                print(f"ilegal char {current_char}")
                self.has_more = False
                return False, current_char
        else:
            if current_char == "(":
                self.expected_closers.append(")")
            if current_char == "[":
                self.expected_closers.append("]")
            if current_char == "{":
                self.expected_closers.append("}")
            if current_char == "<":
                self.expected_closers.append(">")
        self.index += 1
        if self.index == len(self.data):
            self.has_more = False

        return True, ""


if __name__ == "__main__":
    data = get_data()
    vals = []
    for d in data:
        chuncker = Chuncker(d)
        while chuncker.has_more:
            t, v = chuncker.move_string()
        if not t:
            vals.append(v)
    count_vals = {}
    for v in vals:
        if v not in count_vals:
            count_vals[v] = 0
        count_vals[v] += 1
    total = 0
    for k, v in count_vals.items():
        total += chuncker.close_char_values[k] * v
    print(total)
