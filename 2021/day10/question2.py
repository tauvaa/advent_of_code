import os

OPENERS = list("{([<")
CLOSERS = list("})]>")
OPEN_CLOSERS = dict(zip(OPENERS, CLOSERS))
CLOSER_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}


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


def get_closers(instring):
    openers = []
    expected_closers = []
    for c in instring:
        if c in OPENERS:
            expected_closers.append(OPEN_CLOSERS[c])
        if c in CLOSERS:
            expected_closers.pop(-1)
    expected_closers.reverse()
    return expected_closers


def calculate_score(closer_list):
    point_totals = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for v in closer_list:
        score *= 5
        score += point_totals[v]
    return score


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [line.strip() for line in f]
    data = [x for x in data if find_invalid(x) is None]
    return data


if __name__ == "__main__":
    data = get_data()

    ecs = [get_closers(x) for x in data]
    scores = [calculate_score(x) for x in ecs]
    scores.sort()
    scores.sort()
    middle = int(len(scores)/2)
    print(scores[middle])

    # ec = get_closers("[({(<(())[]>[[{[]{<()<>>")
    # print(calculate_score(ec))
    # scores = list(map(find_invalid, data))
    # scores = [x for x in scores if x is not None]
    # scores = list(map(lambda x: CLOSER_POINTS[x], scores))

    # print(sum(scores))
