import os

with open(os.path.join(os.path.dirname(__file__), "data", "data")) as f:
    data = [list(line.strip()) for line in f]


def find_most_common(pos, arr):
    one_count, zero_count = 0, 0
    for a in arr:
        if a[pos] == "1":
            one_count += 1
        elif a[pos] == "0":
            zero_count += 1
    if one_count >= zero_count:
        return "1"
    return "0"


def get_dec_from_bin(binnum):

    binnum = list(binnum)
    binnum.reverse()
    rbnum = [(int(x) + 1) % 2 for x in binnum]
    binnum = "".join(binnum)
    rbnum = "".join(map(str, rbnum))
    dnum = 0
    rnum = 0
    for i in range(len(binnum)):
        dnum += int(binnum[i]) * (2 ** i)
        rnum += int(rbnum[i]) * (2 ** i)
    # print(binnum)
    return dnum


def question1():
    binnum = ""
    for i in range(len(data[0])):
        binnum += find_most_common(i, data)
    get_dec_from_bin(binnum)


def question2():
    def make_new_array(array, keep_val, pos):
        new_arr = []
        for a in array:
            if a[pos] == keep_val:
                new_arr.append(a)
        return new_arr

    def find_most_common(array, position):
        one_count, zero_count = 0, 0
        for a in array:
            if a[position] == "1":
                one_count += 1
            elif a[position] == "0":
                zero_count += 1
        if one_count >= zero_count:
            return "1"
        return "0"

    def find_least_common(array, position):
        one_count, zero_count = 0, 0
        for a in array:
            if a[position] == "1":
                one_count += 1
            elif a[position] == "0":
                zero_count += 1
        if one_count < zero_count:
            return "1"
        return "0"

    most_common = data.copy()
    least_common = data.copy()
    for i in range(len(data[0])):
        mc = find_most_common(most_common, i)
        lc = find_least_common(least_common, i)
        if len(most_common) > 1:
            most_common = make_new_array(most_common, mc, i)
        if len(least_common) > 1:
            least_common = make_new_array(least_common, lc, i)

    x = get_dec_from_bin("".join(most_common[0]))
    y = get_dec_from_bin("".join(least_common[0]))
    print(x * y)


if __name__ == "__main__":
    question2()
