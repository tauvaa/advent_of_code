import os


def make_point(point_string):
    x, y = point_string.split(",")
    x = int(x.strip().split("=")[1])
    y = int(y.strip().split("=")[1])
    return (x, y)


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
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
    if point in sensors:
        return True
    for sensor, beacon_distance in sensors.items():
        if beacon_distance >= manahaton_distance(point, sensor):
            return False
    return True


if __name__ == "__main__":
    data = get_data()
    sensors = {}
    beacons = []
    for d in data:
        sensor, beacon = d
        beacons.append(beacon)
        sensors[sensor] = manahaton_distance(sensor, beacon)
    nobeak_counter = 0
    row_range = 20000000
    for i in range(-row_range, row_range):
        if i % 10000 == 0:
            print(i)
        point = (i, 2000000)

        if point in beacons:
            continue
        if not check_point(sensors=sensors, point=point):
            print(point)
            nobeak_counter += 1
    print(nobeak_counter)
