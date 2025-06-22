def get_data():
    grid, movements = [], ""
    in_grid = True
    with open("data.txt") as f:
        for line in f:
            if line == "\n":
                in_grid = False
                continue
            if in_grid:
                grid.append(line.strip())
            else:
                movements += line.strip()
    grid = [list(x) for x in grid]
    return grid, movements


class Grid:
    OPENSPACE = "."
    BOX = "O"
    WALL = "#"

    def __init__(self, grid, movements) -> None:
        self.grid = grid
        self.movements = list(movements)
        self.max_grid_height = len(grid)
        self.max_grid_width = len(grid[0])
        self.rob_position = (0, 0)
        self.grid_positions = [
            (i, j)
            for i in range(self.max_grid_height)
            for j in range(self.max_grid_width)
        ]
        self.find_robot()

    def get_point(self, point):
        i, j = point
        return self.grid[i][j]

    def find_robot(self):
        for p in self.grid_positions:
            if self.get_point(p) == "@":
                self.rob_position = p
                return

    def get_box_cordinates(self):
        cords = []
        for p in self.grid_positions:
            if self.get_point(p) == self.BOX:
                cords.append(p)
        return cords
    def calcuate_value(self):
        cords = self.get_box_cordinates()
        total = 0
        for c in cords:
            total += 100*c[0] + c[1]
        return total

    def move_up(self):
        self.move(direction=[-1, 0])

    def move_down(self):
        self.move(direction=[1, 0])

    def move_left(self):
        self.move(direction=[0, -1])

    def move_right(self):
        self.move(direction=[0, 1])

    def move(self, direction):
        num_steps = 1
        current_pos = self.rob_position
        next_pos = tuple((direction[i] + current_pos[i] for i in range(2)))

        while self.get_point(next_pos) not in (".", "#"):
            current_pos = next_pos
            next_pos = tuple((direction[i] + current_pos[i] for i in range(2)))
            num_steps += 1
        if self.get_point(next_pos) == ".":
            self.grid[self.rob_position[0]][self.rob_position[1]] = "."
            self.grid[self.rob_position[0] + direction[0]][
                self.rob_position[1] + direction[1]
            ] = "@"
            if num_steps == 1:
                self.rob_position = next_pos
            else:
                self.rob_position = (
                    self.rob_position[0] + direction[0],
                    self.rob_position[1] + direction[1],
                )
                self.grid[next_pos[0]][next_pos[1]] = self.BOX

    def __str__(self):
        to_ret = ["".join(g) for g in self.grid]
        return "\n".join(to_ret)


if __name__ == "__main__":
    g, m = get_data()
    grid = Grid(g, m)

    counter = 0
    for movement in grid.movements:
        if movement == ">":
            grid.move_right()
        elif movement == "<":
            grid.move_left()
        elif movement == "^":
            grid.move_up()
        elif movement == "v":
            grid.move_down()
        counter += 1
        # if counter > 3:
        #     break
    print(grid)
    val = grid.calcuate_value()
    print(val)
