import os
from typing import List


class Box:
    def __init__(self, position) -> None:
        self.position = position
        self.left = position
        self.right = (position[0], position[1] + 1)

    def get_above_cords(self):
        return (self.left[0] - 1, self.left[1]), (self.right[0] - 1, self.right[1])

    def get_below_cords(self):
        return (self.left[0] + 1, self.left[1]), (self.right[0] + 1, self.right[1])

    def get_left_cords(self):
        return (self.left[0], self.left[1] - 1)

    def get_right_cords(self):
        return (self.right[0], self.right[1] + 1)

    def move_up(self):
        x, y = self.left
        self.left = (x - 1, y)

        x, y = self.right
        self.right = (x - 1, y)
        self.position = self.left

    def move_down(self):
        x, y = self.left
        self.left = (x + 1, y)

        x, y = self.right
        self.right = (x + 1, y)
        self.position = self.left

    def move_left(self):
        x, y = self.left
        self.left = (x, y - 1)

        x, y = self.right
        self.right = (x, y - 1)
        self.position = self.left

    def move_right(self):
        x, y = self.left
        self.left = (x, y + 1)

        x, y = self.right
        self.right = (x, y + 1)
        self.position = self.left

    def __repr__(self) -> str:
        return f"left: {self.left} | right: {self.right}"


def get_data():
    data = []
    moves = ""
    data_values = True
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:

        for line in f:
            if line.strip() == "":
                data_values = False
                continue
            if data_values:
                data.append(list(line.strip()))
            else:
                moves += line.strip()
    return translate_data(data), moves


def translate_data(data):
    to_ret = []
    for line in data:
        to_app = []
        for val in line:
            if val == "#":
                to_app.extend(["#", "#"])
            elif val == ".":
                to_app.extend([".", "."])
            elif val == "@":
                to_app.extend(["@", "."])
            elif val == "O":
                to_app.extend(["[", "]"])
            else:
                raise RuntimeError(f"{val} is not a valid character")
        to_ret.append(to_app)
    return to_ret


class Grid:
    def __init__(self, data, moves) -> None:
        self.moves = list(moves)
        self.grid_width = len(data[0])
        self.grid_length = len(data)
        self.data = data
        self.box_positions = {}
        self.grid_positions = [
            (i, j) for i in range(len(self.data)) for j in range(len(self.data[0]))
        ]
        self.wall_positions = set(
            [point for point in self.grid_positions if data[point[0]][point[1]] == "#"]
        )
        self.position = (0, 0)
        for i, j in self.grid_positions:
            if data[i][j] == "@":
                self.position = (i, j)
        self.initialize_box_postions(data)

    def get_new_position(self, point, direction):
        px, py = point
        dx, dy = direction
        return (px + dx, py + dy)

    def get_box(self, point):
        value = self.get_cord_value(point)
        if value == "[":
            return self.box_positions.get(point)
        if value == "]":
            return self.box_positions.get((point[0], point[1] - 1))

    def get_cord_value(self, point):
        if point in self.wall_positions:
            return "#"
        if point in self.box_positions:
            return "["
        if point == self.position:
            return "@"
        if tuple((point[0], point[1] - 1)) in self.box_positions:
            return "]"
        return "."

    def initialize_box_postions(self, data):
        for i, j in self.grid_positions:
            if data[i][j] == "[":
                self.box_positions[(i, j)] = Box((i, j))

    def __str__(self) -> str:
        grid = [["" for _ in range(self.grid_width)] for _ in range(self.grid_length)]

        for point in self.grid_positions:
            i, j = point
            grid[i][j] = self.get_cord_value(point)
        grid = ["".join(x) for x in grid]
        return "\n".join(grid)

    def move_left(self):
        direction = [0, -1]
        next_position = self.get_new_position(self.position, direction)
        next_value = self.get_cord_value(next_position)
        if next_value == "#":
            return
        if next_value == ".":
            self.position = (
                self.position[0] + direction[0],
                self.position[1] + direction[1],
            )
            return
        boxes = []
        box = self.get_box(next_position)
        assert isinstance(box, Box)
        if self.get_cord_value(box.get_left_cords()) == "#":
            return
        while box is not None:
            if self.get_cord_value(box.get_left_cords()) == "#":
                return
            assert isinstance(box, Box)
            boxes.append(box)
            next_position = self.get_new_position(box.position, direction)
            box = self.get_box(next_position)
        for b in boxes:
            self.box_positions.pop(b.position)
            b.move_left()
            self.box_positions[b.position] = b
        self.position = self.get_new_position(self.position, direction)

    def move_right(self):
        direction = [0, 1]
        next_position = self.get_new_position(self.position, direction)
        next_value = self.get_cord_value(next_position)
        if next_value == "#":
            return
        if next_value == ".":
            self.position = self.get_new_position(self.position, direction)
            return
        boxes = []
        box = self.get_box(next_position)
        assert isinstance(box, Box)
        if self.get_cord_value(box.get_right_cords()) == "#":
            return
        while box is not None:
            if self.get_cord_value(box.get_right_cords()) == "#":
                return
            boxes.append(box)
            next_position = self.get_new_position(box.right, direction)
            box = self.get_box(next_position)
        for b in boxes:
            self.box_positions.pop(b.position)
            b.move_right()
            self.box_positions[b.position] = b
        self.position = self.get_new_position(self.position, direction)

    def move_up(self):
        direction = [-1, 0]
        next_position = self.get_new_position(self.position, direction)
        next_value = self.get_cord_value(next_position)
        if next_value == "#":
            return
        if next_value == ".":
            self.position = next_position
            return
        box = self.get_box(next_position)

        assert isinstance(box, Box)
        unchecked_boxes = [box]
        boxes = []
        while unchecked_boxes:
            box = unchecked_boxes.pop()
            lb, rb = box.get_above_cords()
            lb_box = self.get_box(lb)
            rb_box = self.get_box(rb)
            if self.get_cord_value(lb) == "#" or self.get_cord_value(rb) == "#":
                return
            if lb_box:
                unchecked_boxes.append(lb_box)
            if rb_box:
                unchecked_boxes.append(rb_box)
            boxes.append(box)
        boxes = set(boxes)
        keep_pos = []
        for b in boxes:
            if b.position not in keep_pos:
                self.box_positions.pop(b.position)
            b.move_up()
            self.box_positions[b.position] = b
            keep_pos.append(b.position)
        self.position = self.get_new_position(self.position, direction)

    def move_down(self):
        direction = [1, 0]
        next_position = self.get_new_position(self.position, direction)
        next_value = self.get_cord_value(next_position)
        if next_value == "#":
            return
        if next_value == ".":
            self.position = next_position
            return
        box = self.get_box(next_position)

        assert isinstance(box, Box)
        unchecked_boxes = [box]
        boxes = []
        while unchecked_boxes:
            box = unchecked_boxes.pop()
            lb, rb = box.get_below_cords()
            lb_box = self.get_box(lb)
            rb_box = self.get_box(rb)
            if self.get_cord_value(lb) == "#" or self.get_cord_value(rb) == "#":
                return
            if lb_box:
                unchecked_boxes.append(lb_box)
            if rb_box:
                unchecked_boxes.append(rb_box)
            boxes.append(box)
        boxes = set(boxes)
        keep_pos = []
        for b in boxes:
            if b.position not in keep_pos:
                self.box_positions.pop(b.position)
            b.move_down()
            self.box_positions[b.position] = b
            keep_pos.append(b.position)
        self.position = self.get_new_position(self.position, direction)

    def run(self):
        counter = 0
        for m in self.moves:
            counter += 1
            # if counter > 4:
            #     return
            if m == "v":
                # print("moving down")
                self.move_down()
            elif m == "^":
                # print("moving up")
                self.move_up()
            elif m == ">":
                # print("moving right")
                self.move_right()
            elif m == "<":
                # print("moving left")
                self.move_left()

    def get_closest_row_wall(self, box):
        return box.left[1]

    def get_closest_column_wall(self, box):
        return box.left[0]


if __name__ == "__main__":
    data, moves = get_data()
    grid = Grid(data, moves)
    grid.run()
    print(grid)
    total = 0
    for k, b in grid.box_positions.items():
        total += 100 * grid.get_closest_column_wall(b) + grid.get_closest_row_wall(b)
    print(total)
