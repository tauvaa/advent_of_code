import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read()
    data = data.split("\n")
    data = list(filter(lambda x: x != "", data))
    # print(data)
    to_app = []
    to_ret = []
    for d in data:
        if d[0] == "$" and len(to_app) > 0:
            to_ret.append(to_app)
            to_app = []
        to_app.append(d)
    to_ret.append(to_app)
    return to_ret


class RunCommands:
    def __init__(self):
        self.current_path = []
        self.dir_sizes = {}

    def get_current_path(self):
        return ".".join(self.current_path)

    def change_dir(self, new_dir):
        # print(new_dir)
        if new_dir == "..":
            self.current_path.pop(-1)
        else:
            self.current_path.append(new_dir)

    def list_dir(self, list_output):
        path = self.get_current_path()
        directories = list(filter(lambda x: x.startswith("dir"), list_output))
        directories = [path + "." + x.split()[1] for x in directories]
        files = list(filter(lambda x: not x.startswith("dir"), list_output))
        files = [int(x.split()[0]) for x in files]
        file_sizes = sum(files)
        self.dir_sizes[path] = {
            "file_size": file_sizes,
            "directories": directories,
        }

    def run_command(self, command):
        if len(command) == 1:
            command = command[0]
            new_dir = command.split()[-1]
            self.change_dir(new_dir)
        else:
            self.list_dir(command[1:])


def find_dir_size(directory, dir_sizes):
    # print(dir_sizes, directory)

    if len(directory["directories"]) == 0:
        return directory["file_size"]
    else:
        return directory["file_size"] + sum([find_dir_size(dir_sizes[d], dir_sizes) for d in directory["directories"]])

commands = get_data()
runner = RunCommands()
for c in commands:
    runner.run_command(c)
# runner.run_command(commands[0])
# print(runner.current_path)
dir_sizes = runner.dir_sizes
big_files = []
total_size = 0
for f in dir_sizes:
    tocheck = find_dir_size(dir_sizes[f], dir_sizes)
    if tocheck <= 100000:
        total_size += tocheck
        print(total_size)
