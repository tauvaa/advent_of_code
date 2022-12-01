import os
from functools import reduce

import numpy as np


def make_base_data():

    with open(
        os.path.join(os.path.dirname(__file__), "data", "baseprod")
    ) as f:
        data = [l.strip() for l in f if l != ""]
    return data


def get_expanded_grid():
    num_added = 2
    data = make_base_data()
    data = list(map(lambda x: list(map(int, list(x))), data))
    # print(data)

    def adjust_tile(data, num):
        to_ret = data
        for i in range(num):

            to_ret = [[(x + 1) if x < 9 else 1 for x in y] for y in to_ret]
        return to_ret

    def make_grid(data):
        columns = []
        rows = []
        # print(data[0])
        for row in data:
            # print(row)
            rows.append("".join(map(str, row)))

        return "".join(rows)

    grid = []
    for row in range(num_added):
        to_app = []

        for column in range(num_added):
            to_app.append(adjust_tile(data, row + column))
        grid.append(to_app)
    def expand_row(row, block_number, num_blocks):
        expanded_row = []
        for i in range(num_blocks):

            add_block = i + block_number
            for r in row:
                to_app = add_block + r
                to_app = (to_app - 1) % 9
                expanded_row.append(to_app)
        expanded_row = [x + 1 for x in expanded_row]
        return expanded_row
    
    all_rows = []
    for i in range(5):

        for row in data:

            all_rows.append(expand_row(row, i, 5))
    all_rows = ["".join([str(x) for x in row]) for row in all_rows]
    return "\n".join(all_rows)


if __name__ == "__main__":
    data = get_expanded_grid()
    print(data)
