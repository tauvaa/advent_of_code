import os


def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "data1")
    with open(file_path) as f:
        data = [int(line.strip()) for line in f]
    return data


if __name__ == "__main__":
    counter = 0

    data = get_data()
    previous = None
    for d in data:
        if previous is not None:
            if previous < d:
                counter += 1
        previous = d
    print(counter)

