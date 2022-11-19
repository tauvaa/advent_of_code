import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        start_string = ""
        hit_rules = False
        rules = []
        for line in f:
            if line == "\n":
                hit_rules = True
            else:
                if hit_rules:
                    rules.append(line.strip())
                else:
                    start_string += line.strip()
        return rules, start_string


def handle_rules(inrule):
    x, y = inrule.split(" -> ")
    return x, y


def insert_string(instring, rules):

    to_ret = instring[0]
    for i in range(len(instring) - 1):
        current_chars = instring[i : i + 2]
        if current_chars in rules:
            to_add = rules[current_chars] + current_chars[1]
        else:
            to_add = current_chars[1]
        to_ret += to_add
    return to_ret


def get_numbers(string):
    counters = {}
    for x in string:
        if x not in counters:
            counters[x] = 0
        counters[x] += 1
    return counters


if __name__ == "__main__":
    rules, start_string = get_data()
    rules = list(map(handle_rules, rules))
    rules = dict(rules)
    for i in range(10):
        print(f"step number: {i}")
        start_string = insert_string(start_string, rules)
    counters = get_numbers(start_string)
    count_list = list(zip(counters.keys(), counters.values()))
    count_list.sort(key=lambda x: x[1])
    max_count, min_count = count_list[-1], count_list[0]
    print(max_count, min_count)
    print(max_count[1] - min_count[1])
