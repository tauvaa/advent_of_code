import math
import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [
            [[int(k) for k in y.split(",")] for y in r]
            for r in [x.split(" -> ") for x in [x.strip() for x in f]]
        ]
    return data


def get_line_points(p1, p2):
    if p1[0] != p2[0] and p1[1] != p2[1]:
        return ()
    all_points = [tuple(p1)]
    slope = [p2[i] - p1[i] for i in range(2)]
    fact = math.sqrt(sum([x ** 2 for x in slope]))
    slope = [int(x / fact) for x in slope]
    current_point = list(p1)

    while tuple(current_point) != tuple(p2):
        current_point[0] += slope[0]
        current_point[1] += slope[1]
        all_points.append(tuple(current_point))

    return all_points

if __name__ == "__main__":
    
    all_data = {}
    data = get_data()
    for d in data:
        points = get_line_points(*d)
        for p in points:
            if p not in all_data:
                all_data[p] = 0
            all_data[p] += 1
    print(len([x for x in all_data.values() if x > 1]))
