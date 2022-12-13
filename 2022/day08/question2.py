import functools
import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [x.strip() for x in f]
    data = [list(x) for x in data]
    return data


def get_view(data, point):
    x, y = point
    point_value = data[x][y]
    # check up
    up_counter, down_counter = 0, 0
    for i in range(x - 1, 0 - 1, -1):
        up_counter += 1
        if data[i][y] >= point_value:
            break

    for i in range(x + 1, len(data)):
        down_counter += 1
        if data[i][y] >= point_value:
            break

    left_counter, right_counter = 0, 0
    for i in range(y - 1, 0 - 1, -1):
        left_counter += 1
        if data[x][i] >= point_value:
            break

    for i in range(y + 1, len(data)):
        right_counter += 1
        if data[x][i] >= point_value:
            break
    return up_counter, down_counter, left_counter, right_counter


if __name__ == "__main__":
    data = get_data()
    tall_trees = []
    max_view = 0
    for point in [
        (x, y) for x in range(len(data)) for y in range(len(data[0]))
    ]:
        dist = functools.reduce(lambda x, y: x * y, get_view(data, point))
        if dist > max_view:
            max_view = dist
            
    print(max_view)

