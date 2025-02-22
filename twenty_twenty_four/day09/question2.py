import os
from typing import List
def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        data = f.read()
        data = data.strip()
    return data
class FileBlock:
    def __init__(self, file_id, space):
        self.file_id = file_id
        self.space = int(space)

    def __str__(self):
        return f"file id: {self.file_id} space: {self.space}"

    def __repr__(self):
        return f"file id: {self.file_id} space: {self.space}"


def clean_data(data):
    to_ret = []
    for i, size in enumerate(data):
        if i % 2 == 0:
            id_ = int(i / 2)
        else:
            id_ = None
        to_ret.append(FileBlock(id_, size))
    return to_ret


class FileSystem:
    def __init__(self, data):
        self.files: List[FileBlock] = clean_data(data)
        self.moved_files = set()

    def find_free_mem(self, size, file_index):
        for i, file in enumerate(self.files):
            if i >= file_index:
                return
            if file.space >= size and file.file_id is None:
                return i

    def find_next_move_file(self):
        for i in range(len(self.files)):
            index = len(self.files) - 1 - i
            current_file = self.files[index]

            if (
                current_file.file_id is not None
                and current_file.file_id not in self.moved_files
            ):
                return index

    def swap_files(self, free_mem_file_index, file_index):
        assert free_mem_file_index < file_index
        file = self.files.pop(file_index)
        self.files.insert(file_index, FileBlock(None, file.space))
        self.files.insert(free_mem_file_index, file)
        self.files[free_mem_file_index + 1].space -= file.space
        if self.files[free_mem_file_index + 1].space == 0:
            self.files.pop(free_mem_file_index + 1)
        elif self.files[free_mem_file_index + 2].file_id is None:
            free_mem_file1 = self.files.pop(free_mem_file_index + 1)
            free_mem_file2 = self.files.pop(free_mem_file_index + 2)
            self.files.insert(
                free_mem_file_index + 1,
                FileBlock(None, free_mem_file1.space + free_mem_file2.space),
            )

    def move_files(self):
        counter = 0
        while True:
            move_file_index = self.find_next_move_file()
            move_file: FileBlock = self.files[move_file_index]
            if move_file.file_id == 0:
                break
            free_mem_file_index = self.find_free_mem(move_file.space, move_file_index)
            if free_mem_file_index is not None:
                self.swap_files(free_mem_file_index, move_file_index)
            self.moved_files.add(move_file.file_id)
            counter +=1
            # if counter == 4:
            #     break
    def get_file_string(self):
        file_string = ""
        for f in self.files:
            if f.file_id is None:
                char = "."
            else:
                char = str(f.file_id)
            file_string += char * int(f.space)
        return file_string
    def get_file_check_sum(self, offset, file):
        total = 0
        for i in range(file.space):
            total += (i+offset) * int(file.file_id)
        return total
    def get_check_sum(self):
        total = 0
        offset = 0
        for i, val in enumerate(self.files):
            if val.file_id is not None:
                total += self.get_file_check_sum(offset, val)
            offset += val.space
            print(offset, val.file_id)
        return total
        


if __name__ == "__main__":
    data = get_data()
    fs = FileSystem(data)
    # print(fs.files)
    fs.move_files()
    # print(fs.files)
    # print(fs.moved_files)
    print(fs.get_file_string())
    print(fs.get_check_sum())
