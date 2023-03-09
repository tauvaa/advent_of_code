import os


def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "data2")
    with open(file_path) as f:
        data = [line.strip() for line in f]
    return data


def solution():
    position = [0, 0]
    aim = 0
    data = get_data()
    for d in data:
        motion, amount = d.split(" ")
        amount = int(amount)
        if motion == "forward":
            position[0] += amount
            position[1] += amount * aim
        if motion == "up":
            aim -= amount
        if motion == "down":
            aim += amount
    print(position[0] * position[1])


if __name__ == "__main__":
    solution()
