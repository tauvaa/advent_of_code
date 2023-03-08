import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f]
    data = [list(x) for x in data]
    return data


if __name__ == "__main__":
    data = get_data()
    tall_trees = []
    perimeter = 2*len(data) + 2*len(data[0]) - 4

    for i in range(1, len(data) - 1):
        for j in range(1, len(data[0]) - 1):
            tree_size = data[i][j]
            tree_row = data[i]
            right_trees = [data[i][k] for k in range(j + 1, len(data[0]))]
            left_trees = [data[i][k] for k in range(0, j)]

            if all(x < tree_size for x in right_trees) or all(
                x < tree_size for x in left_trees
            ):

                tall_trees.append((i, j))
            up_trees, down_trees = [], []
            for k in range(0, i):
                up_trees.append(data[k][j])
            for k in range(i + 1, len(data)):
                down_trees.append(data[k][j])
            if all(x < tree_size for x in up_trees) or all(
                x < tree_size for x in down_trees
            ):
                tall_trees.append((i, j))
    tall_trees = set(tall_trees)
    print(len(tall_trees) + perimeter)
