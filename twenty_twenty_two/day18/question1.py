import os
import datetime as dt


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
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


if __name__ == "__main__":
    start_time = dt.datetime.now().timestamp() 
    data = get_data()

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
    counter = 0
    for c in all_clusters:
        counter += c.num_faces

    print(counter)
    end_time = dt.datetime.now().timestamp()

    print(f"Time: {end_time - start_time}")
