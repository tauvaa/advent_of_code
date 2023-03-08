import os


def make_point(point_string):
    x, y = point_string.split(",")
    x = int(x.strip().split("=")[1])
    y = int(y.strip().split("=")[1])
    return (x, y)


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [l.strip() for l in f]
    data = [[x.split("at")[1].strip() for x in d.split(":")] for d in data]
    data = [[make_point(x) for x in d] for d in data]
    return data


def manahaton_distance(x, y):
    to_ret = 0
    for i, v in enumerate(x):
        to_ret += abs(v - y[i])
    return to_ret


def check_point(sensors, point):
    for sensor, beacon_distance in sensors.items():
        if beacon_distance >= manahaton_distance(point, sensor):
            return False
    return True


def calculate_row_coverage(row, sensor, distance):
    x, y = sensor
    if abs(row - y) > distance:
        return ()
    v1 = distance - abs(row - sensor[1]) + sensor[0]
    v2 = -(distance - abs(row - sensor[1])) + sensor[0]
    maxval, minval = max(v1, v2), min(v1, v2)
    return minval, maxval


def get_max_coverage(cover_points, max_point, min_point=0):
    cover_points = list(
        filter(lambda x: len(x) > 0 and x[1] >= 0, cover_points)
    )
    cover_points.sort()
    to_ret = [*cover_points[0]]
    for i in range(len(cover_points) - 1):
        current_point = cover_points[i]
        next_point = cover_points[i + 1]
        if to_ret[1] + 1 >= next_point[0]:
            to_ret[1] = max(next_point[1], to_ret[1])
        else:
            return to_ret
    return to_ret


if __name__ == "__main__":
    data = get_data()
    sensors = {}
    beacons = {}
    for d in data:
        sensor, beacon = d
        sensors[sensor] = manahaton_distance(sensor, beacon)
        if beacon not in beacons:
            beacons[beacon] = 0
        beacons[beacon] = max(
            beacons[beacon], manahaton_distance(sensor, beacon)
        )
    print(sensors)

    maxrange = 4000000
    all_covers = []
    counter = 0
    for r in range(maxrange):
        counter += 1
        if counter % 100000 == 0:
            print(counter)
        for sensor, distance in sensors.items():
            all_covers.append(calculate_row_coverage(r, sensor, distance))
        cover = get_max_coverage(all_covers, maxrange)
        if cover[1] < maxrange:
            print(r, "here", cover)
            break
        all_covers = []
    for i in range(maxrange + 1):
        point = (i, r)
        if check_point(sensors, point):
            print(point)
            print(point[0] * 4000000 + point[1])
            break
