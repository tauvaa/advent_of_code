import os
def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read()
    data = data.split("\n")
    data = [x for x in data if x != ""]
    return data


def find_marker(instrin):
    marker = ""
    counter = 0
    for char in instrin:
        if len(marker) >= 14:
            if len(marker) == len(set(marker)):
                return counter
            marker = marker[1:]
        marker += char
        counter += 1


if __name__ == "__main__":
    data = get_data()
    for d in data:
        print(find_marker(d))
