import os
from collections import defaultdict


def get_data():
    rules, updates = [], []
    hit_updates = False
    with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
        for l in f:
            if l == "\n":
                hit_updates = True
            elif hit_updates:
                updates.append(l.strip())
            else:
                rules.append(l.strip())
    return rules, updates


def handle_update(update):
    return [int(x) for x in update.split(",")]


def handle_rules(rules):
    trules = defaultdict(set)
    for rule in rules:
        before, after = rule.split("|")
        before, after = int(before), int(after)
        trules[before].add(after)
    return trules

    
def check_valid_update(update, rules):
    checked_pages = set()
    for page in update:
        if len(checked_pages.intersection(rules[page])) != 0:
            return False
        checked_pages.add(page)
    return True
        
if __name__ == "__main__":
    rules, updates = get_data()
    updates = list(map(handle_update, updates))
    rules = handle_rules(rules)
    valid_updates = []
    for update in updates:
        if check_valid_update(update, rules):
            valid_updates.append(update[int(len(update)/2)])
    print(sum(valid_updates))


