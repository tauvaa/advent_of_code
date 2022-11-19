import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [list(x.strip()) for x in f]
        data = [[int(x) for x in y] for y in data]

    return data


class Octopus:
    def __init__(self, energy_level):
        self.energy_level = energy_level
        self.has_flashed = False

    def next_step(self):
        self.energy_level += 1

    def flash(self):
        self.has_flashed = True


class Grid:
    def __init__(self, data):
        self.data = data
        self.max_rows = len(data)
        self.max_columns = len(data[0])
        self.flash_counter = 0

    def check_all_flash(self):
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                if not self.data[i][j].has_flashed:
                    return False
        return True

    def next_step(self):
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                self.data[i][j].has_flashed = False
        for row in self.data:
            for column in row:
                column.next_step()
        self.flash_points()

    def get_flash_points(self):
        points_found = False
        flash_points = []
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                if (
                    self.data[i][j].energy_level >= 10
                    and not self.data[i][j].has_flashed
                ):
                    flash_points.append((i, j))
                    self.flash_counter += 1
                    points_found = True
        return flash_points

    def flash_adjacent(self, point):
        adjpoints = self.get_adjacent(point)
        for row, column in adjpoints:
            self.data[row][column].energy_level += 1

    def flash_points(self):
        fp = self.get_flash_points()
        while len(fp) > 0:
            for p in fp:
                self.flash_adjacent(p)
                self.data[p[0]][p[1]].flash()
            fp = self.get_flash_points()
        self.clear_points()

    def clear_points(self):
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                if self.data[i][j].energy_level > 10:
                    self.data[i][j].energy_level = 0

    def get_adjacent(self, point):
        row, column = point
        valid_rows, valid_columns = [row], [column]
        if row + 1 < self.max_rows:
            valid_rows += [row + 1]
        if row - 1 >= 0:
            valid_rows += [row - 1]
        if column + 1 < self.max_columns:
            valid_columns += [column + 1]
        if column - 1 >= 0:
            valid_columns += [column - 1]
        valid_points = [(r, c) for r in valid_rows for c in valid_columns]
        return valid_points

    def __str__(self):
        to_print = [",".join(str(x.energy_level) for x in y) for y in self.data]
        to_print = "\n".join(to_print)
        return to_print


if __name__ == "__main__":
    data = get_data()
    data = [[Octopus(x) for x in y] for y in data]
    grid = Grid(data)
    for i in range(1000):

        grid.next_step()
        if grid.check_all_flash():
            print(grid)
            break
    print(i + 1)
