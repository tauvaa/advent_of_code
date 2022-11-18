import os


def get_number(string):
    valid_numbers = {2: 1, 4: 4, 3: 7, 7: 8}
    set_numbers = {
        "cdfbe": 5,
        "gcdfa": 2,
        "fbcad": 3,
        "cefabd": 9,
        "cdfgeb": 6,
        "cagedb": 0,
    }
    if len(string) in valid_numbers:
        return valid_numbers[len(string)]
    # for s in set_numbers:
    #     if set(s) == set(string):
    #         return set_numbers[s]
    # return 0
    # return string


def get_data():
    def sort_letters(string):
        # print(string)
        string = list(string)
        string.sort()
        return "".join(string)

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read()
    indata = []
    outdata = []
    data = list(filter(lambda x: x != "", data.split("\n")))

    # print(data)
    for d in data:
        idata, odata = d.split("|")
        idata = idata.strip().split()
        odata = odata.strip().split()
        indata.append(idata)
        outdata.append(odata)
    # outdata = list(map(sort_letters, outdata))
    out_ret, in_ret = [], []
    for o in outdata:

        out_ret.append(list(map(sort_letters, o)))

    for i in indata:
        in_ret.append(list(map(sort_letters, i)))
    return in_ret, out_ret


def get_string(innum):
    to_ret = ""
    for num in innum:
        # print(num)
        to_ret += str(get_number(num))
    return to_ret


def get_knew_letters(invals):
    known_letters = {}
    for l in invals:
        if get_number(l) is not None:
            known_letters[get_number(l)] = l
    return known_letters


def get_nine(know_letters, innumbers):
    sixnine = list(filter(lambda x: len(x) == 6, innumbers))
    seven = set(know_letters[7])
    four = set(know_letters[4])

    fourseven = seven.union(four)
    fourseven = list(fourseven)
    fourseven.sort()
    for val in sixnine:
        t = set(val).intersection(set(fourseven))
        if len(t) == 5:
            return val


def get_zero(known_letters, innumbers):
    innumbers = list(filter(lambda x: len(x) == 6, innumbers))
    four = set(known_letters[4])
    nine = set(known_letters[9])
    seven = set(known_letters[7])
    for num in innumbers:
        if (
            len(four.intersection(num)) == 3
            and len(nine.intersection(num)) == 5
            and len(seven.intersection(num)) == 3

        ):
            return num


def get_six(known_letters, innumbers):
    innumbers = list(filter(lambda x: len(x) == 6, innumbers))
    nine = set(known_letters[9])
    zero = set(known_letters[0])
    for num in innumbers:
        if set(num) != nine and set(num) != zero:
            return num


def get_two(know_letters, innumbers):
    innumbers = list(filter(lambda x: len(x) == 5, innumbers))
    four = set(known_letters[4])
    for num in innumbers:
        if len(set(num).intersection(four)) == 2:
            return num


def get_three(known_letters, innumbers):
    innumbers = list(filter(lambda x: len(x) == 5, innumbers))
    one = set(known_letters[1])
    two = set(known_letters[2])
    for num in innumbers:
        if (
            len(one.intersection(set(num))) == 2
            and len(two.intersection(set(num))) == 4
        ):
            return num


def get_five(known_letters, innumbers):
    innumbers = list(filter(lambda x: len(x) == 5, innumbers))
    three = known_letters[3]
    two = known_letters[2]
    for num in innumbers:
        if num != three and num != two:
            return num


def make_string(known_letters, invals):

    temp_dic = dict(zip(known_letters.values(), map(str, known_letters.keys())))
    to_ret = ""
    for l in invals:
        to_ret += temp_dic[l]

    return int(to_ret)


if __name__ == "__main__":
    indata, outdata = get_data()
    counter = 0
    for i, d in enumerate(outdata):

        known_letters = get_knew_letters(d + indata[i])
        nine = get_nine(known_letters, indata[i])

        known_letters[9] = nine
        zero = get_zero(known_letters, indata[i])
        known_letters[0] = zero
        six = get_six(known_letters, indata[i])
        known_letters[6] = six
        two = get_two(known_letters, indata[i])
        known_letters[2] = two
        three = get_three(known_letters, indata[i])
        known_letters[3] = three
        five = get_five(known_letters, indata[i])
        known_letters[5] = five
        make_string(known_letters, d)
        counter += make_string(known_letters, d)
    print(counter)
