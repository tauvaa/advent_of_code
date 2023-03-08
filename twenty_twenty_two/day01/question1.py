import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        all_elvs = []
        elf = 0
        for x in f:
            if x == "\n":
                all_elvs.append(elf)
                elf = 0
            else:
                elf += int(x.strip())
    return all_elvs


if __name__ == "__main__":
    data = get_data()
    print(max(data))

