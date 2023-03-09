import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [x.strip() for x in f]
    return data


def get_most_common(data, idx):
    ones, zeros = [], []
    for d in data:
        if d[idx] == "1":
            ones.append(d)
        else:
            zeros.append(d)
    return zeros if len(zeros) > len(ones) else ones


def get_least_common(data, idx):
    ones, zeros = [], []
    for d in data:
        if d[idx] == "1":
            ones.append(d)
        else:
            zeros.append(d)
    return zeros if len(zeros) <= len(ones) else ones


def get_oxygen():
    data = get_data()
    idx = 0
    while len(data) > 1:
        data = get_most_common(data, idx)
        idx += 1
        idx %= len(data[0])
    return data[0]


def get_co2():
    data = get_data()
    idx = 0
    while len(data) > 1:
        data = get_least_common(data, idx)
        idx += 1
        idx %= len(data[0])
    return data[0]


if __name__ == "__main__":
    oxygen, co2 = get_oxygen(), get_co2()
    oxygen = int(oxygen, 2)
    co2 = int(co2, 2)

    print(oxygen * co2)
