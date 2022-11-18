import os

valid_numbers = [2, 4, 3, 7]

def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read()
    data = data.split("\n")
    data = filter(lambda x: x != "", data)
    data = [x.split("|")[1].strip() for x in data]
    data = [x.split() for x in data]

    return data


if __name__ == "__main__":
    data = get_data()
    print(data)
    all_nums = []
    for d in data:
        all_nums += d
    counter = 0
    for num in all_nums:
        if len(num) in valid_numbers:
            counter += 1
    print(counter)
