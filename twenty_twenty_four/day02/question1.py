import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [[int(k) for k in x.split(" ")] for x in f]
    return data


def is_safe(line):
    total_offset = 0
    for i in range(len(line) - 1):
        current = line[i]
        next_value = line[i + 1]
        updated_offset = next_value - current
        if not (
            abs(total_offset)
            < abs(total_offset + updated_offset)
            < (abs(total_offset) + 4)
        ):
            return False
        total_offset = updated_offset + total_offset
    return True


if __name__ == "__main__":
    counter = 0
    for i, line in enumerate(get_data()):
        if is_safe(line):
            # print(i)
            counter += 1
    print(counter)
