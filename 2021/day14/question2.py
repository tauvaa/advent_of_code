import json
import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
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


def get_letter_counts(instring, num_iter):
    for i in range(num_iter):
        instring = insert_string(instring, rules)
    return get_numbers(instring)


def get_all_letter_counts(force=False):
    filename = "total_counts.json"
    if force or filename not in os.listdir(os.path.dirname(__file__)):

        letter_counts = {}
        for x in rules:
            print(f"starting: {x}")
            letter_counts[x] = get_letter_counts(x, 20)
        with open(os.path.join(os.path.dirname(__file__), filename), "w+") as f:
            f.write(json.dumps(letter_counts))
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        letter_counts = json.loads(f.read())
    return letter_counts


if __name__ == "__main__":
    rules, start_string = get_data()
    rules = list(map(handle_rules, rules))
    rules = dict(rules)
    total_counts = {x: 0 for x in rules.values()}
    letter_counts = get_all_letter_counts()

    for _ in range(20):
        start_string = insert_string(start_string, rules)
    stl = len(start_string)
    for i in range(len(start_string) - 1):
        if i % 10000 == 0:
            print(i/stl)
        segment = start_string[i : i + 2]
        add_char = segment[1]
        total_counts[add_char] -= 1
        to_add = letter_counts[segment]
        for k, v in to_add.items():
            total_counts[k] += v
    total_counts[start_string[-1]] += 1
    stotals = list(zip(total_counts.keys(), total_counts.values()))
    stotals.sort(key=lambda x: x[1])
    max_count, min_count = stotals[-1], stotals[0]

    print(max_count, min_count)
    print(max_count[1] - min_count[1])
