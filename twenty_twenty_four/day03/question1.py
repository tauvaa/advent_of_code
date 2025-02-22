from functools import reduce
from os.path import dirname, join


def get_data():
    with open(join(dirname(__file__), "data.txt")) as f:
        data = f.read()
    return data


def handle_data(instring):
    in_mul = False
    all_mulls = []
    index = 0
    first_num, second_num = "", ""
    number = "first"
    while index < len(instring):
        char = instring[index]
        if char == "m" and not in_mul and index < len(instring) - 5:
            if instring[index : index + 4] == "mul(":
                in_mul = True
                index += 4
                char = instring[index]
            else:
                in_mul = False
        if in_mul:
            # print(char)
            if char.isdigit():
                if number == "first":
                    first_num += char
                else:
                    second_num += char
            elif char == "," and number == "first":
                print(first_num)
                number = "second"
            elif char == ")":
                if (
                    number == "second"
                    and 0 < len(second_num) < 4
                    and 0 < len(first_num) < 4
                ):
                    all_mulls.append([int(first_num), int(second_num)])
                in_mul = False
                number = "first"
                first_num, second_num = "", ""

                # print(first_num, second_num)
            else:
                in_mul = False
                number = "first"
                first_num, second_num = "", ""

        index += 1
    return all_mulls


if __name__ == "__main__":
    to_mul = handle_data(get_data())
    print(reduce(lambda x, y: x + y, map(lambda a: a[0] * a[1], to_mul)))
