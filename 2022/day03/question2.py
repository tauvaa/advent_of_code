
import os
import string


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [l.strip() for l in f if l.strip() != ""]

    to_ret = []
    counter = 0
    to_app = []
    for d in data:
        if counter == 3:
            counter = 0
            to_ret.append(to_app)
            to_app = []
        to_app.append(d)
        counter += 1
    to_ret.append(to_app)

    return to_ret



if __name__ == "__main__":

    data = get_data()
    temp = []
    for d in data:
        ta = []
        for t in d:
            ta.append(set(list(t)))
        temp.append(ta)
    data = temp
    all_letters = []
    for d in data:
        counter = {}
        for t in d:
            for char in t:
                if char not in counter:
                    counter[char] = 0
                counter[char] += 1
        counter = list(zip(counter.keys(), counter.values()))
        counter = [x for x in counter if x[1] == 3]
        all_letters.append(counter[0][0])
    total = 0
    for a in all_letters:
        total += list(string.ascii_letters).index(a) + 1
    print(total)

        

