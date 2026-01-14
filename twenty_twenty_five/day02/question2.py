def get_data():
    with open("data.txt") as f:
        data = f.read()
    data = data.strip().split(",")
    data = [list(map(int, x.split("-"))) for x in data]
    return data


def get_splits(string, split_len):
    splits = []
    for i in range(0, len(string) - split_len + 1, split_len):
        splits.append(string[i : i + split_len])
    return splits


def check_splits_equal(splits):
    if len(splits) == 0:
        return False
    to_check = splits.pop(0)
    for split in splits:
        if split != to_check:
            return False
    return True


def check_multi(string):
    string_len = len(string)
    for i in range(1, int(len(string) / 2) + 1):
        if string_len % i == 0:
            if check_splits_equal(get_splits(string, i)):
                return True
    return False
def main():
    data = get_data()
    total = 0
    for start, end in data:
        for i in range(start, end + 1):
            string_val = str(i)
            if check_multi(string_val):
                total += i
    print(total)

if __name__ == "__main__":
    main()

