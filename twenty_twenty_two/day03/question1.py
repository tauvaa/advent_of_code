
import os
import string


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [l.strip() for l in f if l.strip() != ""]

    to_ret = []
    for d in data:
        half_point = int(len(d) / 2)
        lower, upper = d[0:half_point], d[half_point:]

        to_ret.append((lower, upper))
    return to_ret


if __name__ == "__main__":

    data = get_data()
    same_items = []

    for compart in data:
        similar = set()
        lower, upper = compart

        for l in lower:
            if l in upper:

                similar.add(*l)
        for s in similar:
            same_items.append(s)
    total=0
    for k in same_items:
        total += list(string.ascii_letters).index(k) + 1
    print(total)
