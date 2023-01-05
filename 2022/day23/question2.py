import datetime as dt
import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read()
    data = data.split("\n")
    data = [list(x) for x in data if x != ""]
    return data


class Grid:
    def __init__(self, data):
        self.data = data

        self.check_points = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "W": (0, -1),
            "NW": (-1, -1),
            "NE": (-1, 1),
            "SW": (1, -1),
            "SE": (1, 1),
        }
        self.propse_directions = ["N", "S", "W", "E"]
        self.elf_positions = set()
        self.get_elf_positions()

    def get_elf_positions(self):
        self.elf_positions = set([
            (x, y)
            for x in range(len(self.data))
            for y in range(len(self.data[0]))
            if self.data[x][y] == "#"
        ])

    def propose_move(self, point, direction):
        if direction == "N":
            to_check = ("N", "NE", "NW")
            if all((self.check_elf(point, x) is None for x in to_check)):
                return False
            else:
                return not any((self.check_elf(point, x) for x in to_check))

        elif direction == "S":
            to_check = ("S", "SE", "SW")
            if all((self.check_elf(point, x) is None for x in to_check)):
                return False
            else:
                return not any((self.check_elf(point, x) for x in to_check))

        elif direction == "E":
            to_check = ("E", "SE", "NE")
            if all((self.check_elf(point, x) is None for x in to_check)):
                return False
            else:
                return not any((self.check_elf(point, x) for x in to_check))

        elif direction == "W":
            to_check = ("W", "SW", "NW")
            if all((self.check_elf(point, x) is None for x in to_check)):
                return False
            else:
                return not any((self.check_elf(point, x) for x in to_check))

    def check_elf(self, point, to_check):
        x, y = point
        tc_x, tc_y = self.check_points[to_check]
        x, y = (x + tc_x, y + tc_y)
        return (x, y) in self.elf_positions

    def get_move_point(self, point, direction):
        return (
            point[0] + self.check_points[direction][0],
            point[1] + self.check_points[direction][1],
        )

    def get_propositions(self):
        to_ret = {}

        for point in self.elf_positions:
            if all(
                (
                    self.check_elf(point, x) or self.check_elf(point, x) is None
                    for x in self.check_points
                )
            ):
                continue
            skip_point = True
            for d in self.check_points:
                if self.check_elf(point, d):
                    skip_point = False
            if skip_point:
                continue

            for d in self.propse_directions:
                if self.propose_move(point, d):
                    to_ret[point] = self.get_move_point(point, d)
                    break
        return to_ret

    def get_valid_moves(self):
        to_ret = {}
        props = self.get_propositions()
        for k, v in props.items():
            if len(list(x for x in props.values() if x == v)) == 1:
                to_ret[k] = v
        return to_ret

    def take_step(self):
        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            return
        for old in valid_moves:
            self.elf_positions.remove(old)
        for new in valid_moves.values():
            self.elf_positions.add(new)

        self.propse_directions = [
            self.propse_directions[(i + 1) % len(self.propse_directions)]
            for i in range(len(self.propse_directions))
        ]
        return True

    def get_num_empty(self):
        min_row, max_row = min([x[0] for x in self.elf_positions]), max(
            [x[0] for x in self.elf_positions]
        )
        min_col, max_col = min([x[1] for x in self.elf_positions]), max(
            [x[1] for x in self.elf_positions]
        )
        max_row += 1
        max_col += 1
        return (max_row - min_row) * (max_col - min_col) - len(
            self.elf_positions
        )

    def __str__(self) -> str:
        min_row, max_row = min([x[0] for x in self.elf_positions]), max(
            [x[0] for x in self.elf_positions]
        )
        min_col, max_col = min([x[1] for x in self.elf_positions]), max(
            [x[1] for x in self.elf_positions]
        )
        max_row += 1
        max_col += 1
        grid = []
        for i in range(min_row, max_row):
            col = []
            for j in range(min_col, max_col):
                col.append(".")
            grid.append(col)
        for elf in self.elf_positions:
            elf_off = (elf[0] - min_row, elf[1] - min_col)
            print(elf_off)
            grid[elf_off[0]][elf_off[1]] = "#"

        return "\n".join(["".join(row) for row in grid])


if __name__ == "__main__":
    data = get_data()

    grid = Grid(data)
    counter = 0
    while grid.take_step():
        counter += 1
        if counter % 10 == 0:
            print(counter)
    print(counter + 1)
