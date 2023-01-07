import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f.readlines()]

    return data


def converter(innum):
    translators = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    total = 0
    for i, dig in enumerate(innum):
        to_add = 5 ** (len(innum) - 1 - i) * translators[dig]
        total += to_add
    return total


def inverter(num):
    pass


def base_5(num):
    powers = []
    p = 0
    while 5 ** p <= num:
        p += 1

    while num > 0:
        starter = 4
        while starter * 5 ** p > num:
            starter -= 1
        num -= starter * 5 ** p
        powers.append(starter)
        indexer = len(powers) - 1

        while powers[indexer] > 2:

            if powers[indexer] == 3:
                powers[indexer - 1] += 1
                powers[indexer] = -2
            elif powers[indexer] == 4:
                powers[indexer - 1] += 1
                powers[indexer] = -1
            indexer -= 1
        p -= 1
    while p > -1:
        powers.append(0)
        p -=1
    for i in range(len(powers)):
        if powers[i] == -2:
            powers[i] = "="
        if powers[i] == -1:
            powers[i] = "-"
    powers = map(str, powers)
    powers = "".join(powers)

    return powers


if __name__ == "__main__":
    numbers = get_data()

    p = 0
    x = 34561628468940
    while 5 ** p < x:
        p += 1
    print(converter("01"))
    x = base_5(x)
    print("answer: ", x)
    print(converter(x))
