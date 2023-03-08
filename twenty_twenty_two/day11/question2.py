import math
import os
from fractions import gcd


def round_number(num):
    lower = int(num)
    upper = lower + 1
    if abs(num - lower) < abs(num - upper):
        return lower
    return upper


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = []
        to_app = []
        for l in f:
            if l == "\n":
                data.append(to_app)
                to_app = []
            else:
                to_app.append(l.strip())
        data.append(to_app)
    return data


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level

    def relief(self):
        self.worry_level = int(self.worry_level / 3)


class Monkey:
    def __init__(self, monkey_configuration, moder):
        (
            _,
            starting_items,
            operation,
            test,
            if_true,
            if_false,
        ) = monkey_configuration
        starting_items = starting_items.split(":")[1]
        starting_items = [int(x) for x in starting_items.split(",")]
        starting_items = [Item(int(x)) for x in starting_items]
        self.items = starting_items
        self.operation = operation.split(":")[1].strip()
        test = test.split(":")[1].strip()
        self.test = test
        self.if_true = if_true.split(":")[1].strip()
        self.if_false = if_false.split(":")[1].strip()
        self.to_throw = []
        self.times_inspected = 0
        self.moder = moder

    def throw_item(self, throw_to, item_index):

        self.to_throw.append({"throw_to": throw_to, "item_index": item_index})

    def test_item(self, item, item_index):
        test = self.test.split(" ")[-1]
        divisor = int(test)
        item.worry_level %=self.moder 
        if item.worry_level % divisor == 0:

            self.run_true(item_index)
        else:
            self.run_false(item_index)

    def add_item(self, item):
        self.items.append(item)

    def run_true(self, item_index):
        monkey = self.if_true.split(" ")[-1]
        monkey = int(monkey)
        self.throw_item(monkey, item_index)

    def run_false(self, item_index):
        monkey = self.if_false.split(" ")[-1]
        monkey = int(monkey)
        self.throw_item(monkey, item_index)

    def perform_operation(self, item: Item):
        operation = self.operation.split("=")[1].strip()
        arg1, op, arg2 = operation.split(" ")
        arg1 = item.worry_level if arg1 == "old" else int(arg1)
        arg2 = item.worry_level if arg2 == "old" else int(arg2)
        arg1, arg2 = int(arg1), int(arg2)
        greatest_common_div = math.gcd(arg1, arg2)
        # arg1 = arg1 // greatest_common_div
        # arg2 = arg2 // greatest_common_div
        if op == "+":
            item.worry_level = (arg1 + arg2)
        else:
            item.worry_level = (arg1 * arg2)
        self.times_inspected += 1
        # item.relief()

    def loop_items(self):
        for i, item in enumerate(self.items):
            self.perform_operation(item)
            self.test_item(item, item_index=i)

        self.to_throw.sort(key=lambda x: x["item_index"])
        self.to_throw.reverse()


if __name__ == "__main__":
    data = get_data()
    moder = 1
    for d in data:
        moder *= int(d[3].split(" ")[-1])

    monkeys = [Monkey(d, moder) for d in data]
    for counter in range(10000):
        for monkey in monkeys:
            monkey.loop_items()
            for throw_it in monkey.to_throw:
                to_throw, item_index = [
                    throw_it["throw_to"],
                    throw_it["item_index"],
                ]
                item = monkey.items.pop(item_index)
                monkeys[to_throw].add_item(item)
            monkey.to_throw = []
        if counter > 700:
            print("counter: ", counter)
    inspections = [m.times_inspected for m in monkeys]
    inspections.sort(reverse=True)
    print(inspections[0] * inspections[1])
    print(inspections)
