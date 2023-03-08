import os
import sys

import numpy as np


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [int(line.strip()) for line in f]
    return data


def get_new_index(start_point, shift_num, list_len):

    if shift_num < 0:
        adder = -1
    else:
        adder = 1
    current_point = start_point
    for i in range(abs(shift_num)):
        current_point += adder
        if current_point == 0 and adder < 0:
            current_point = list_len - 2

        elif current_point == list_len - 1 and adder > 0:
            current_point = 1
    return current_point


def solution():
    data = get_data()
    # data = [1, 2, 3, 4, 4]

    def wrap_list(
        data,
    ):
        base_list = data.copy()
        data_index = list(range(len(data)))
        # for i in range(num_wraps):

        for i in range(len(data_index)):

            current_index = data_index[i]
            d = data[current_index]
            new_index = get_new_index(current_index, d, len(data))
            data.pop(current_index)
            data.insert(new_index, d)
            for j, v in enumerate(data_index):
                if v >= current_index and v <= new_index:
                    data_index[j] -= 1
                # if v >= new_index:
                #     data_index[j] += 1
                if v == current_index:
                    data_index[j] = new_index

            print(
                data, current_index, data_index, [data[i] for i in data_index]
            )
            try:
                assert tuple([data[i] for i in data_index]) == tuple(base_list)
            except Exception as err:
                print(tuple([data[i] for i in data_index]), tuple(base_list))

                raise (err)
        return data

    data = wrap_list(data)
    iindex = data.index(0)

    print(
        sum(map(lambda x: data[(iindex + x) % len(data)], (1000, 2000, 3000)))
    )


if __name__ == "__main__":
    # d = [4, -2, 5, 6, 7, 8, 9]
    # ni = get_new_index(1, -2, len(d))
    # d.pop(1)
    # d.insert(ni, -2)
    # print(d)
    solution()
