import os


def get_data():
    boards = []
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [line.strip() for line in f]
        numbers = data.pop(0)
        data.pop(0)
    numbers = [int(x) for x in numbers.split(",")]
    board = []
    for line in data:
        if line == "":
            boards.append(board)
            board = []
        else:
            board.append([int(x) for x in line.split()])
    boards.append(board)

    return numbers, boards


class Board:
    def __init__(self, data) -> None:
        self.data = data
        self.elms = [
            (i, j)
            for i in range(len(self.data))
            for j in range(len(self.data[0]))
        ]

    def call_number(self, number):
        for elm in self.elms:
            i, j = elm
            if self.data[i][j] == number:
                self.data[i][j] = "x"

    def check_board(self):
        for row in self.data:
            if all([x == "x" for x in row]):
                return True
        for i in range(len(self.data[0])):
            if all([x[i] == "x" for x in self.data]):
                return True
        return False

    def calculate_board(self):
        total = 0
        for i, j in self.elms:
            if self.data[i][j] != "x":
                total += self.data[i][j]
        return total

    def __str__(self):
        to_print = ""
        for r in self.data:
            r = [str(x) for x in r]

            to_print += ",".join(r)
            to_print += "\n"
        return to_print


if __name__ == "__main__":
    numbers, boards = get_data()
    boards = [Board(board) for board in boards]
    found = False
    for n in numbers:
        for b in boards:
            b.call_number(n)
            if b.check_board():
                print(n, b)
                print(b.calculate_board() * n)
                found = True
                break
        if found:
            break
