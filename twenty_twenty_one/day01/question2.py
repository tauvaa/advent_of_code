import os


def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "data2")
    with open(file_path) as f:
        data = [int(line.strip()) for line in f]
    return data


if __name__ == "__main__":
    counter = 0

    data = get_data()
    previous = None
    for i in range(len(data) - 2):
        current = sum(data[i : i + 3])
        if previous is not None:

            if previous < current:
                counter += 1
        previous = current
    print(counter)
