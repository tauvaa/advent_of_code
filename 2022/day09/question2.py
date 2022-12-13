import enum
import os


class Instructions(enum.Enum):
    left = "L"
    right = "R"
    up = "U"
    down = "D"


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [x.strip() for x in f if not x.startswith("#")]
    to_ret = []
    for d in data:
        inst = d.split()
        inst, num = Instructions(inst[0]), int(inst[1])
        for k in range(num):
            to_ret.append(inst)

    return to_ret


class Knot:
    def __init__(self):
        self.head_position = (0, 0)
        self.tail_position = (0, 0)
        self.tail_positions = []

    def take_step(self, instruction):
        """take a step instruction (right, left, up, down)"""
        if instruction == Instructions.down:
            self.move_down()
        elif instruction == Instructions.up:
            self.move_up()
        elif instruction == Instructions.right:
            self.move_right()
        elif instruction == Instructions.left:
            self.move_left()
        self.check_distance()

    def move_tail_left_right(self, distance):
        if distance[0] > 1:
            self.tail_position = (
                self.tail_position[0] + 1,
                self.tail_position[1],
            )
        elif distance[0] < -1:
            self.tail_position = (
                self.tail_position[0] - 1,
                self.tail_position[1],
            )
        if distance[1] > 1:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] + 1,
            )
        elif distance[1] < -1:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] - 1,
            )
        self.tail_positions.append(self.tail_position)

    def move_diagonal(self, distance):
        print("move diagonal")
        x, y = distance
        if x < 0:
            self.tail_position = (
                self.tail_position[0] - 1,
                self.tail_position[1],
            )
        if x > 0:
            self.tail_position = (
                self.tail_position[0] + 1,
                self.tail_position[1],
            )
        if y < 0:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] - 1,
            )
        if y > 0:
            self.tail_position = (
                self.tail_position[0],
                self.tail_position[1] + 1,
            )
        # print(self.head_position, self.tail_position)
        self.tail_positions.append(self.tail_position)

    def check_distance(self):
        distance = tuple(
            (self.head_position[i] - self.tail_position[i] for i in range(2))
        )
        if sum(map(abs, distance)) == 3:
            self.move_diagonal(distance=distance)
        else:
            self.move_tail_left_right(distance=distance)

    def move_right(self):
        print("moved right")
        x, y = self.head_position
        self.head_position = (x, y + 1)

    def move_left(self):
        print("moved left")
        x, y = self.head_position
        self.head_position = (x, y - 1)

    def move_up(self):
        print("moved up")
        x, y = self.head_position
        self.head_position = (x + 1, y)

    def move_down(self):
        print("moved down")
        x, y = self.head_position
        self.head_position = (x - 1, y)


class Grid:
    def __init__(self, size):
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.offset = 25

    def fill_point(self, point, symbol="x"):
        x, y = point
        x = x + self.offset
        y = y + self.offset
        self.grid[x][y] = symbol

    def __str__(self):
        rows = ["".join(x) for x in self.grid]
        rows.reverse()
        return "\n".join(rows)


class Solution:
    def __init__(self):
        self.all_knots = [Knot() for _ in range(10)]
        self.grid = Grid(50)

    def take_step(self, instruction):
        for i, knot in enumerate(self.all_knots):
            if i == 0:
                knot.take_step(instruction)
            else:
                knot.head_position = self.all_knots[i - 1].tail_position
                knot.check_distance()

    def run(self, instructions):

        print("running...")
        # instructions = instructions[0:10]
        for i in instructions:
            self.take_step(i)
        # for i, knot in  enumerate(self.all_knots):
        #     self.grid.fill_point(knot.head_position,str(i))
        self.grid.fill_point((0,0), "x")

        print(self.grid)


        tp = self.all_knots[-2].tail_positions
        tp = set(tp)
        print(len(tp))
        # for x in tp:
        #     print(x)
        #     self.grid.fill_point(x)
        # print(self.grid)

        # print(len(tp))
        # print(self.all_knots[-1].tail_positions)
        for knot in self.all_knots:
            print(knot.head_position)

        # for i, k in enumerate(self.all_knots):
        #     print(i, k.head_position)


if __name__ == "__main__":
    data = get_data()
    print(data)
    print(len(data))
    print(data)
    solution = Solution()
    solution.run(data)
    g = Grid(50)
    g.fill_point((0, 0))

    # print(g)
