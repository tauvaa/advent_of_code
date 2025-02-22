import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [list(line.strip()) for line in f]
    return data


def get_xes(data):
    all_points = []
    points = [(i, j) for i in range(len(data)) for j in range(len(data[0]))]
    for point in points:
        i, j = point
        if data[i][j] == "X":
            all_points.append(point)
    return all_points


def check_point(point, data):
    cord_changes = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]
    check_chars = ["X", "M", "A", "S"]
    counter = 0
    # cord_changes = [(-1, -1)]
    i, j = point
    for idelta, jdelta in cord_changes:
        found_word = True
        for k, char in enumerate(check_chars):
            try:
                if (
                    (not data[i + k * idelta][j + k * jdelta] == char)
                    or (i + k * idelta < 0)
                    or (j + k * jdelta < 0)
                ):
                    found_word = False
            except IndexError as err:

                found_word = False
            if not found_word:
                break
            # print(i + k*idelta, j + k*jdelta)

        if found_word:
            # print(i + k*idelta, j + k*jdelta)
            counter += 1
    return counter


if __name__ == "__main__":
    data = get_data()
    total = 0
    print(data[7][-1])
    for point in get_xes(data):
        total += check_point(point, data)
        print(point, check_point(point, data))
    print(total)
