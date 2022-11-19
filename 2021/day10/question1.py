import os

OPENERS = list("{([<")
CLOSERS = list("})]>")
OPEN_CLOSERS = dict(zip(OPENERS, CLOSERS))
CLOSER_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [line.strip() for line in f]
    return data


def find_invalid(instring):
    openers = []
    expected_closers = []
    for c in instring:
        if c in OPENERS:
            expected_closers.append(OPEN_CLOSERS[c])
        if c in CLOSERS:
            expected_closer = expected_closers.pop(-1)
            if c != expected_closer:
                return c


if __name__ == "__main__":
    data = get_data()
    scores = list(map(find_invalid, data))
    scores = [x for x in scores if x is not None]
    scores = list(map(lambda x: CLOSER_POINTS[x], scores))

    print(sum(scores))

