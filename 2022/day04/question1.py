import os
import string


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = []
        for line in f:
            line = line.strip().split(",")
            line = [list(map(int, x.split("-"))) for x in line]
            data.append(line)

    return data


def cover_point(x, y):
    if x[0] <= y[0] and x[1] >= y[1]:
        return True
    elif y[0] <= x[0] and y[1] >= x[1]:
        return True
    return False


if __name__ == "__main__":
    data = get_data()
    counter = 0
    for d in data:
        if cover_point(*d):
            print(d)
            counter += 1
    print(counter)
