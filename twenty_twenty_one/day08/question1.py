import os


def get_data():
    data = []
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        for line in f:
            line = line.split("|")
            line = [x.strip() for x in line]
            line = [x.split() for x in line]

            data.append(line)

    return data


def count_segments(segs):
    counter = 0
    for s in segs:
        if len(s) in (2, 4, 3, 7):
            counter += 1
    return counter


if __name__ == "__main__":
    data = get_data()
    counter = 0
    for d in data:
        counter += count_segments(d[1])
    print(counter)
