import os

with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
    data = f.read().strip()


def read_in_data(datastring):
    data = datastring.split("\n")
    called_numbers = data.pop(0).split(",")
    called_numbers = list(map(int, called_numbers))
    data.pop(0)
    all_boards = []
    current_board = []
    for line in data:
        if line == "":
            all_boards.append(current_board)
            current_board = []
        else:
            line = [int(x) for x in line.split()]
            current_board.append(line)
    all_boards.append(current_board)
    return called_numbers, all_boards


class Board:
    def __init__(self, data):
        self.data = data

    def check_number(self, number):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] == number:
                    self.data[i][j] = None

    def print_board(self):
        print(self.data)

    def check_column(self, column_number):
        for a in self.data:
            if a[column_number] is not None:
                return False
        return True

    def check_board(self):
        for a in self.data:
            if all(x is None for x in a):
                return True
        for i in range(len(self.data[0])):
            if self.check_column(i):
                return True
        return False

    def sum_board(self):
        board_sum = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] is not None:
                    board_sum += self.data[i][j]
        return board_sum


if __name__ == "__main__":
    called_numbers, all_boards = read_in_data(data)
    boards = list(map(lambda x: Board(x), all_boards))
    board_hit = [False for _ in boards]
    for num in called_numbers:
        for i, board in enumerate(boards):
            board.check_number(num)
            if board.check_board():
                board_hit[i] = True
                boards_hit = all(board_hit)
                if boards_hit:
                    break
                # board.print_board()
                # board_found = True
        if all(board_hit):
            break
    print(board.sum_board() * num)

    print(num)
    board.print_board()
