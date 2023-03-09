import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [[int(k) for k in list(x)] for x in [line.strip() for line in f]]
    return data


class Octupus:
    def __init__(self, energy_level):
        self.energy_level = energy_level
        self.will_flash = False

    def add_level(self):
        self.energy_level += 1
        if self.energy_level > 9:
            self.will_flash = True

    def flash(self):
        self.energy_level = 0
        self.will_flash = False


class OctMap:
    def __init__(self, data) -> None:
        self.max_rows = len(data)
        self.max_cols = len(data[0])
        self.oct_points = [
            (x, y) for x in range(len(data)) for y in range(len(data[0]))
        ]
        self.puses = [
            [Octupus(data[i][j]) for j in range(len(data[0]))]
            for i in range(len(data))
        ]
        self.flashed_points = set()
        self.num_flashes = 0

    def clean_up(self):
        for i, j in self.oct_points:
            pus = self.puses[i][j]
            if pus.will_flash:
                pus.flash()
                self.num_flashes += 1
        self.flashed_points = set()

    def take_step(self):
        for i, j in self.oct_points:
            pus = self.puses[i][j]
            pus.add_level()
            if pus.will_flash and (i, j) not in self.flashed_points:
                self.flashed_points.add((i, j))
                self.flash_pus((i, j))
        self.clean_up()

    def flash_pus(self, point):
        i, j = point
        to_flash = [
            (x, y)
            for x in range(i - 1, i + 2)
            for y in range(j - 1, j + 2)
            if (
                (x, y) != point
                and 0 <= x
                and x < self.max_rows
                and 0 <= y
                and y < self.max_cols
            )
        ]
        for i, j in to_flash:
            pus = self.puses[i][j]
            pus.add_level()
            if pus.will_flash and (i, j) not in self.flashed_points:
                self.flashed_points.add((i, j))
                self.flash_pus((i, j))

    def check_zeros(self):
        for row in self.puses:
            if any([x.energy_level != 0 for x in row]):
                return False
        return True

    def __str__(self):
        rows = [[x.energy_level for x in row] for row in self.puses]
        rows = ["".join(list(map(str, x))) for x in rows]
        rows.append("==================")
        return "\n".join(rows)


if __name__ == "__main__":
    data = get_data()

    om = OctMap(data)

    counter = 0
    while True:
        om.take_step()
        counter += 1
        if om.check_zeros():
            break
    print(om)
    print(counter)
