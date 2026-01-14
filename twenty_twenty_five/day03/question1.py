def get_data():
    with open("data.txt") as f:
        data = [[int(x) for x in line.strip()] for line in f]
    return data


def get_max_value(array, with_last):
    max_value = None
    val_index = None
    for i, val in enumerate(array[0 : len(array) if with_last else len(array) - 1]):
        if max_value is None or max_value < val:
            max_value = val
            val_index = i
    return val_index, max_value


def get_max_two_digit(array):
    _ind, val = get_max_value(array, False)
    assert _ind is not None and val is not None
    if len(array[_ind + 1:]) == 1:
        second_digit = array[-1]
    else:
        _, second_digit = get_max_value(array[_ind + 1 :], True)
    return 10 * val + second_digit
if __name__ == "__main__":
    total = 0
    for d in get_data():
        to_add = get_max_two_digit(d)
        print(to_add)
        total += to_add
    print(total)
