import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [line.strip() for line in f]
    data = list(map(lambda x: [int(k) for k in x.split(",")], data))

    return data


def check_adjacent(cube1, cube2):
    counter = 0
    for i, c in enumerate(cube1):
        c2 = cube2[i]
        if c2 == c:
            counter += 1
        if abs(c - c2) > 1:
            return False
    return counter >= 2


def check_trapped(cube_points):
    all_cubes = [tuple(x) for x in cube_points]
    to_ret = []
    maxx, maxy, maxz = (
        max([x[0] for x in all_cubes]) + 1,
        max([x[1] for x in all_cubes]) + 1,
        max([x[2] for x in all_cubes]) + 1,
    )
    all_points = [
        (x, y, z) for x in range(maxx) for y in range(maxy) for z in range(maxz)
    ]
    for p in all_points:
        if p in all_cubes:

            continue
        counter = 0
        for c in cube_points:
            if check_adjacent(c, p):
                counter += 1
        if counter == 6:
            to_ret.append(p)
    return to_ret


class Cluster:
    def __init__(self, initial_point) -> None:
        self.num_cubes = 1
        self.cube_points = [initial_point]
        self.num_faces = 6

    def check_adjacent(self, cube):
        num_adjacent = 0
        for c in self.cube_points:
            if check_adjacent(c, cube):
                num_adjacent += 1

        return num_adjacent

    def add_cube(self, cube):
        num_adjacent = self.check_adjacent(cube)

        if num_adjacent == 0:
            return False
        self.cube_points.append(cube)
        self.num_faces = self.num_faces + 6 - 2 * num_adjacent
        self.num_cubes += 1
        return True

    def __add__(self, obj):
        to_ret = Cluster(self.cube_points[0])
        to_ret.cube_points = self.cube_points + obj.cube_points
        to_ret.num_cubes = self.num_cubes + obj.num_cubes
        to_ret.num_faces = self.num_faces + obj.num_faces
        return to_ret


def make_clusters(data):
    data = data.copy()
    print(data)
    cluster = Cluster(data.pop(0))
    all_clusters = [cluster]
    while data:
        print("len all clusters", len(all_clusters))
        to_add = data.pop(0)
        found_it = False
        adjacent_clusters = []
        for i, v in enumerate(all_clusters):
            if v.check_adjacent(to_add):
                adjacent_clusters.append(i)
        if len(adjacent_clusters) > 1:
            adjacent_clusters.sort(reverse=True)
            to_comb = []
            for i in adjacent_clusters:
                to_comb.append(all_clusters.pop(i))
            new_clust = to_comb.pop(0)
            while to_comb:
                new_clust = new_clust + to_comb.pop(0)
            all_clusters.append(new_clust)

        for clust in all_clusters:
            if clust.add_cube(to_add):
                print("found")
                found_it = True
                break
        if not found_it:
            print("not found")
            all_clusters.append(Cluster(to_add))
    return all_clusters


def istrapped(point, cube_points):
    all_cubes = [tuple(x) for x in cube_points]
    to_ret = []
    maxx, maxy, maxz = (
        max([x[0] for x in all_cubes]) + 1,
        max([x[1] for x in all_cubes]) + 1,
        max([x[2] for x in all_cubes]) + 1,
    )
    air_points = [
        (x, y, z)
        for x in range(maxx)
        for y in range(maxy)
        for z in range(maxz)
        if (x, y, z) not in all_cubes
    ]
    all_points = [point]
    while len(all_points) > 0:
        print(len(all_points))
        current_point = all_points.pop()
        x, y, z = current_point
        if x >= maxx - 1 or y >= maxy - 1 or z >= maxz - 1:
            print("returning!!")
            return to_ret, False
        to_ret.append(current_point)
        # print(all_points)
        for mover in (1, -1):
            new_point = (x + mover, y, z)
            if (
                new_point in air_points
                and new_point not in to_ret
                and new_point not in all_points
            ):
                all_points.append(new_point)

            new_point = (x, y + mover, z)
            if (
                new_point in air_points
                and new_point not in to_ret
                and new_point not in all_points
            ):
                all_points.append(new_point)

            new_point = (x, y, z + mover)
            if (
                new_point in air_points
                and new_point not in to_ret
                and new_point not in all_points
            ):
                all_points.append(new_point)
                # print(new_point, maxx, maxx, maxz, len(to_ret), len(all_points))
    print("returninig!!!")
    return to_ret, True


if __name__ == "__main__":

    data = get_data()
    all_clusters = make_clusters(data)

    face_counter = 0
    all_points = []
    for c in all_clusters:
        face_counter += c.num_faces
        all_points += c.cube_points
    all_points = list(map(tuple, all_points))
    maxx = max([x[0] for x in all_points]) + 1
    maxy = max([x[1] for x in all_points]) + 1
    maxz = max([x[2] for x in all_points]) + 1
    air_points = [
        (x, y, z)
        for x in range(maxx)
        for y in range(maxy)
        for z in range(maxz)
        if (x, y, z) not in all_points
    ]
    trapped_points = []
    c = 0
    found_points = set()
    for a in air_points:
        print(len(found_points), "found")
        if a in found_points:
            c += 1
            continue
        tp, trapped = istrapped(a, all_points)
        found_points = found_points.union(set(tp))
        if trapped:
            trapped_points.extend(tp)
        c += 1

        print("counter: ", c)
    tcount = 0
    for c in make_clusters(trapped_points.copy()):
        tcount += c.num_faces
    print(face_counter - tcount)
