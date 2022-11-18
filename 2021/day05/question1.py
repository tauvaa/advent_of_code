import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip()
    data = data.split("\n")
    data = list(map(lambda x: x.split(" -> "), data))
    array = []
    for d in data:
        array.append([d[0].split(","), d[1].split(",")])
    to_ret = []
    for a, b in array:
        if a[0] == b[0] or a[1] == b[1]:
            to_ret.append([a, b])
    return to_ret


def find_lines(points):
    p1, p2 = points
    p1 = list(map(int, p1))
    p2 = list(map(int, p2))
    to_ret = []
    if p1[0] == p2[0]:
        if p1[1] > p2[1]:
            for i in range(p2[1], p1[1] + 1):
                to_ret.append(tuple((p1[0], i)))
        else:
            for i in range(p1[1], p2[1] + 1):
                to_ret.append(tuple((p1[0], i)))
    elif p1[1] == p2[1]:
        if p1[0] > p2[0]:
            for i in range(p2[0], p1[0] + 1):
                to_ret.append(tuple((i, p1[1])))
        else:
            for i in range(p1[0], p2[0] + 1):
                to_ret.append(tuple((i, p1[1])))

    return to_ret


if __name__ == "__main__":
    all_lines = {}
    data = get_data()

    # print(find_lines(data[0]))
    for d in data:
        for p in find_lines(d):
            if p in all_lines:
                all_lines[p] += 1
            else:
                all_lines[p] = 1
    print(all_lines)
    print(len(list(filter(lambda x: x > 1, all_lines.values()))))
