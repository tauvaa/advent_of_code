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

def get_invalid_updates(updates, rules):
    in_valid_updates = []
    for update in updates:
        if not check_valid_update(update, rules):
            in_valid_updates.append(update)
    return in_valid_updates
def make_valid_update(update, rules):
    new_update = []
    for to_add in update:
        added_page = False
        for i, page in enumerate(new_update):
            if page in rules[to_add]:
                new_update = new_update[0: i] + [to_add] + new_update[i:]
                added_page = True
                break
        if not added_page:
            new_update.append(to_add)
    return new_update




        
if __name__ == "__main__":
    rules, updates = get_data()
    updates = list(map(handle_update, updates))
    rules = handle_rules(rules)
    invalid_updates = get_invalid_updates(updates, rules)
    made_valid_updates = [make_valid_update(u, rules) for u in invalid_updates]
    print(sum([x[int(len(x)/2)] for x in made_valid_updates]))
    


