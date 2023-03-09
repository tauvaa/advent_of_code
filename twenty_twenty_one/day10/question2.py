import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [x.strip() for x in f]
    return data


class Chuncker:
    def __init__(self, data) -> None:
        self.data = data
        self.open_chars = list("([{<")
        self.close_chars = list(")]}>")
        self.close_char_values = {")": 1, "]": 2, "}": 3, ">": 4}
        self.expected_closers = []
        self.index = 0
        self.has_more = True

    def move_string(self):
        current_char = self.data[self.index]
        if current_char in self.close_chars:
            next_close = self.expected_closers.pop(-1)
            if next_close != current_char:
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

    def get_complete_value(self):
        total = 0
        self.expected_closers.reverse()
        for val in self.expected_closers:
            total *= 5
            total += self.close_char_values[val]
        return total


if __name__ == "__main__":
    data = get_data()
    incomplete_chunckers = []
    for d in data:
        chuncker = Chuncker(d)
        while chuncker.has_more:
            t, v = chuncker.move_string()
        if t:
            incomplete_chunckers.append(chuncker)
    scores = [c.get_complete_value() for c in incomplete_chunckers]
    scores.sort()
    score = scores[int(len(scores)/2)]
    print(score)
