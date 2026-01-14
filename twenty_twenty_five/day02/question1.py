def get_data():
    with open("data.txt") as f:
        data = f.read()
    data = data.strip()
    data = data.split(",")
    data = [list(map(int, x.split("-"))) for x in data]

    return data


def is_valid(_id):
    _id = str(_id)
    num_dig = len(_id)
    # print(num_dig)
    if num_dig % 2 != 0:
        return True
    first_half, second_half = _id[0 : int(num_dig / 2)], _id[int(num_dig / 2) :]
    if first_half == second_half:
        return False
    return True


def check_range(lower, upper):
    invalid_ids = []
    for i in range(lower, upper + 1):
        if not is_valid(i):
            invalid_ids.append(i)
    return invalid_ids
if __name__ == "__main__":
    total = []
    for d in get_data():
        total += check_range(*d)
    print(sum(total))
