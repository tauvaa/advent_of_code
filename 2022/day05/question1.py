import os
import string


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read()
    puzzle_in = []
    movement = []
    hit_movement = False

    for d in data.split("\n"):
        if d == "":
            hit_movement = True
        elif hit_movement:
            movement.append(d)
        else:
            puzzle_in.append(d)

    return puzzle_in, movement


class Ship:
    def __init__(self, num_cols):
        self.data = [[] for _ in range(num_cols)]
        self.num_cols = num_cols

    def add_row(self, row):
        nrow = []
        inx = 0
        while inx < len(row):
            nrow.append(row[inx : inx + 3])
            inx += 4
        for i, r in enumerate(nrow):
            # print(i)
            if r != "   ":
                self.data[i].append(r)
    def move_data(self, instruction):
        instruction = instruction.split(" ")
        num_to_move = int(instruction[1])
        move_from = int(instruction[3]) - 1
        move_to = int(instruction[5]) - 1
        for num in range(num_to_move):
            move_box = self.data[move_from].pop(0)
            self.data[move_to] = [move_box] + self.data[move_to]




if __name__ == "__main__":
    puzzle, movement = get_data()
    # print(puzzle)
    ship = Ship(int((len(puzzle[0]) + 1) / 4))
    for i in range(len(puzzle) - 1):
        ship.add_row(puzzle[i])
    print(ship.data)
    for m in movement:

        ship.move_data(m)
    string = ""
    for d in ship.data:
        string += d[0][1]
    print(string)
