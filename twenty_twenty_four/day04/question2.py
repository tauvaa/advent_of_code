import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = f.read().split("\n")
        data = filter(lambda x: x, data)
        data = list(data)
        data = list(map(list, data))
    return data


def get_as(data):
    all_as = []
    for i, j in [(k, l) for k in range(len(data)) for l in range(len(data[0]))]:
        if data[i][j] == "A":
            all_as.append((i, j))
    return all_as


def check_as(point, data):
    i, j = point
    max_i, max_j = len(data) - 1, len(data[0]) - 1
    if i - 1 < 0 or i + 1 > max_i or j - 1 < 0 or j + 1 > max_j:
        return False
    if (
        (data[i - 1][j + 1] == "M" and data[i + 1][j - 1] == "S")
        or (data[i - 1][j + 1] == "S" and data[i + 1][j - 1] == "M")
    ) and (
        (data[i - 1][j - 1] == "M" and data[i + 1][j + 1] == "S")
        or (data[i - 1][j - 1] == "S" and data[i + 1][j + 1] == "M")
    ):
        return True


if __name__ == "__main__":
    data = get_data()
    counter = 0
    for point in get_as(data):
        if check_as(point, data):
            counter += 1
    print(counter)
