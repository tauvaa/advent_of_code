import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f]
    start_string = data.pop(0)
    data.pop(0)
    start = [start_string[i : i + 2] for i in range(len(start_string) - 1)]
    return start_string, start, data


class Poly:
    def __init__(self, data, start_vals, start_string) -> None:
        self.data = [x.split(" -> ") for x in data]
        self.pairs = {x[0]: 0 for x in self.data}
        for pair in start_vals:
            self.pairs[pair] += 1
        all_letters = ""
        for p in self.pairs:
            all_letters += p
        all_letters = set(list(all_letters))
        all_letters = {x: 0 for x in all_letters}
        for s in start_string:
            all_letters[s] += 1
        self.all_letters = all_letters

    def next_step(self):
        new_pairs = self.pairs.copy()
        for pair, num in self.pairs.items():
            if num > 0:
                to_add, new_letter = self.get_poly(pair)
                new_pairs[pair] -= num
                self.all_letters[new_letter] += num
                for val in to_add:
                    new_pairs[val] += num
        self.pairs = new_pairs

    def get_poly(self, pair):
        to_ret = []
        for d in self.data:
            if d[0] == pair:
                to_ret = [d[0][0] + d[1], d[1] + d[0][1]]
                return to_ret, d[1]


if __name__ == "__main__":
    start_string, start, data = get_data()
    pol = Poly(data, start, start_string)
    for _ in range(40):
        pol.next_step()
    pairs = [(v, k) for k, v in pol.all_letters.items()]
    pairs.sort()
    mx, mn = pairs[-1], pairs[0]
    print(mx[0] - mn[0])
