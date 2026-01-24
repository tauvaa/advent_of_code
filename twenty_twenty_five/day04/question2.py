import os


def read_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = [list(line.strip()) for line in f]
    return data


class Grid:
    def __init__(self, data) -> None:
        self.data = data
        self.max_row = len(data)
        self.max_col = len(data[0])
        self.roll_points = self.get_rolls()
        self.to_remove = []

    def get_rolls(self):
        all_points = [(i, j) for i in range(self.max_row) for j in range(self.max_col)]
        roll_points = [p for p in all_points if self.get_point(p) == "@"]
        return roll_points

    def less_than_four_adjacent(self, point):
        row, col = point
        offsets = [
            (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
        ]
        total_adjectent = 0
        for orow, ocol in offsets:
            offset_point = (row + orow, col + ocol)
            if (
                self.max_row > offset_point[0] >= 0
                and self.max_col > offset_point[1] >= 0
            ):
                point_val = self.get_point(offset_point)
                if point_val == "@":
                    total_adjectent += 1
                    # print(offset_point)
                if total_adjectent > 3:
                    return False
        self.to_remove.append(point)
        return True

    def get_point(self, point):
        row, col = point
        return self.data[row][col]

    def remove_rolls(self):
        for row, col in self.to_remove:
            self.data[row][col] = "x"
        self.roll_points = [x for x in self.roll_points if x not in self.to_remove]
        self.to_remove = []
                            
    def run_and_remove(self):
        total = 0
        for point in self.roll_points:
            if self.less_than_four_adjacent(point):
                total += 1
        self.remove_rolls()

        return total


if __name__ == "__main__":
    data = read_data()
    grid = Grid(data)
    total = 0
    while(toadd:= grid.run_and_remove()) > 0:
        total += toadd
    print(total)
