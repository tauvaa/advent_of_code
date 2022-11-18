import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read()
        data = list(map(int, data.split(",")))

    return data


def get_distace(x, y):
    n = abs(x - y)
    return (n*(n+1))/2


def get_total_fuel(points, position):
    total_fuel = 0
    for p in points:
        total_fuel += get_distace(p, position)
    return total_fuel
        


if __name__ == "__main__":
    data = get_data()
    fuel_pos = [(get_total_fuel(data, pos), pos) for pos in range(min(data), max(data) + 1)]
    fuel_pos.sort(key=lambda x: x[0])
    print(fuel_pos[0])
