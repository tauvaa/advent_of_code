import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip().split(",")
        data = list(map(int, data))
    return data


def get_cheapest():
    data = get_data()
    mx, mn = max(data), min(data)
    all_vals = []
    for i in range(mn, mx):
        total = sum([(abs(i - d) * (abs(i - d) + 1)) / 2 for d in data])
        all_vals.append((total, i))
    all_vals.sort()
    return all_vals


if __name__ == "__main__":
    print(get_cheapest()[0])
