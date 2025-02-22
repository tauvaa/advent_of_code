import os

spelled_digits = {
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9
}
def get_numbers(line):
    to_ret = []
    for i, c in enumerate(line):
        if line[i].isdigit():
            to_ret.append(int(c))
        else:
            for k in spelled_digits:
                if line[i:].startswith(k):
                    to_ret.append(spelled_digits[k])


    return to_ret

    

def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "question2")) as f:
        data = f.read()
    data = data.strip()
    data = data.split("\n")
    return data


if __name__ == "__main__":
    data = get_data()
    # print(data)
    # print(get_digits("21n9"))
    # print(get_digits("4nineeightseven2"))
    # print(swap_spelled("nine"))
    print(get_numbers("3eighthree"))
    total = 0
    for line in get_data():
        nums = get_numbers(line)
        current = int(str(nums[0]) + str(nums[-1]))
        total += current
    print(total)


    exit()
    print(swap_spelled("nineeight"))
    print(swap_spelled("seven"))
    print(swap_spelled("52sevenone"))
    for line in get_data():
        s = swap_spelled(line)
        print(s)
        print(get_digits(s))

    total = 0
    for line in data:
        # print(line)
        # print(swap_spelled(line))
        # print(get_digits(swap_spelled(line)))
        total += int(get_digits(swap_spelled(line)))
    print(total)
