import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = f.read()
        data = data.strip()
    return data


class FileInfo:
    def __init__(self, file_id, mem_space):
        self.file_id = file_id
        self.mem_space = mem_space


class Solution:
    def __init__(self, input_string):
        self.dot_string = []
        self.file_space = []
        self.left_index = 0
        self.right_index = 0
        self.make_dot_string(input_string)

    def shift_left_index(self):
        while self.dot_string[self.left_index] != ".":
            self.left_index += 1

    def shift_right_index(self):
        while self.dot_string[self.right_index] == ".":
            self.right_index -= 1

    def swap_mem(self):
        self.shift_left_index()
        self.shift_right_index()
        if self.left_index < self.right_index:
            self.dot_string[self.left_index] = self.dot_string[self.right_index]
            self.dot_string[self.right_index] = "."
            return True
        return False

    def make_dot_string(self, input_string):
        for value, mem in enumerate(input_string):
            print(mem)
            if value % 2 == 0:
                id_num = int(value / 2)
            else:
                id_num = None

            file_ = FileInfo(id_num, mem_space=mem)
            self.file_space.append(file_)
            mem = int(mem)
            self.dot_string.extend(mem * [id_num if id_num is not None else "."])
            self.right_index = len(self.dot_string) -1 
    def get_check_sum(self):
        dot_string = [x for x in self.dot_string if x != "."]
        total = 0
        for i, val in enumerate(dot_string):
            total += i *val
        print(total)

    def solve(self):

        while self.swap_mem():
            pass
        self.get_check_sum()


if __name__ == "__main__":
    data = get_data()
    solution = Solution(data)
    solution.solve()
