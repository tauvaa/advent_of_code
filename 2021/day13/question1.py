import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [l.strip() for l in f]
    tdata = []
    instructions = []
    start_instruct = False
    for d in data:
        if d == "":
            start_instruct = True
        if start_instruct:
            instructions.append(d)
        else:
            tdata.append(d)

    data = tdata
    data = [tuple(map(int, x.split(","))) for x in data]
    instructions = [x for x in instructions if x != ""]

    return data, instructions


def handle_instructions(instruction):
    instruct = instruction.split(" ")[-1]
    axis, line = instruct.split("=")
    return {"axis": axis, "line": int(line)}


class Grid:
    def __init__(self, data):
        self.max_x = max([x[0] for x in data]) + 1
        self.max_y = max([x[1] for x in data]) + 1
        self.points = data
        self.grid = []
        self.build_grid()

    def build_grid(self):
        grid = []
        for j in range(self.max_y):
            to_app = []
            for i in range(self.max_x):
                if (i, j) in self.points:
                    to_app.append("#")
                else:
                    to_app.append(".")
            grid.append(to_app)
        self.grid = grid

    def make_grid(self, grid_cords):
        gcords = "\n".join(["".join(x) for x in grid_cords])
        return gcords

    def set_maxes(self):
        self.max_x = len(self.grid[0])
        self.max_y = len(self.grid)

    def cord_trans_x(self, cord, line):
        return (cord[0], -(cord[1] + 1))

    def cord_trans_y(self, cord, line):
        return (-(cord[0] + 1), cord[1])

    def flip_x(self, line):
        left, right = [], []
        for row in self.grid:
            left.append(row[0:line])
            right.append(row[1 + line :])
        for i in range(len(right)):
            for j in range(len(right[0])):
                if right[i][j] == "#":
                    cord = self.cord_trans_x((i, j), line)
                    left[cord[0]][cord[1]] = "#"
        self.grid = left
        self.set_maxes()

    def flip_y(self, line):
        upper, lower = self.grid[0:line], self.grid[line + 1 :]
        # print(self.make_grid(upper))
        # print("=" * 15)
        # print(self.make_grid(lower))
        # print("=" * 15)
        for i in range(len(lower)):
            for j in range(len(lower[0])):
                if lower[i][j] == "#":
                    tcord = self.cord_trans_y((i, j), line)
                    upper[tcord[0]][tcord[1]] = "#"
        self.grid = upper
        self.set_maxes()

    def get_point_count(self):
        counter = 0
        for row in self.grid:
            for col in row:
                if col == "#":
                    counter += 1
        return counter

    def __str__(self):
        grid = ["".join(x) for x in self.grid]
        grid = "\n".join(grid)
        return grid


if __name__ == "__main__":
    data, instructions = get_data()
    istr = []
    for x in instructions:
        istr.append(handle_instructions(x))
    instructions = istr
    grid = Grid(data)
    for i in instructions:
        if i["axis"] == "x":
            grid.flip_x(i["line"])
        else:
            grid.flip_y(i["line"])
        print(grid.get_point_count())
    print(grid.get_point_count())
    print(grid)
