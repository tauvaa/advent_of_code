import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [x.strip() for x in f]
    return data


def get_bin_strings():
    data = get_data()
    total = len(data)
    epsilon, gamma = "", ""
    for i in range(len(data[0])):
        ones_counter = 0
        for d in data:
            if d[i] == "1":
                ones_counter += 1
        if ones_counter > total / 2:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    return gamma, epsilon


if __name__ == "__main__":
    gamma, epsilon = get_bin_strings()
    print(int(gamma, 2) * int(epsilon, 2))
