"""
rules
If the stone is engraved with the number 0, it is replaced by a stone engraved
with the number 1. 

If the stone is engraved with a number that has an even number of digits, it is
replaced by two stones. The left half of the digits are engraved on the new
left stone, and the right half of the digits are engraved on the new right
stone. (The new numbers don't keep extra leading zeroes: 1000 would become
stones 10 and 0.)    

If none of the other rules apply, the stone is replaced by a new stone; the old
stone's number multiplied by 2024 is engraved on the new stone.
"""
import json
from collections import defaultdict

start_stones = "0 1 10 99 999"
start_stones = start_stones.split(" ")
# start_stones = map(int, start_stones.split(" "))

stone_cache = {}


def split_stone(stone):
    stone = list(stone)
    stone_len = len(stone)
    left_stone = stone[0 : int(stone_len / 2)]
    right_stone = stone[int(stone_len / 2) :]
    left_stone = "".join(left_stone)
    right_stone = "".join(right_stone)
    while right_stone.startswith("0"):
        right_stone = right_stone[1:]
    if right_stone == "":
        right_stone = "0"
    return left_stone, right_stone


def blink(stone_list, step_number):
    to_ret = []
    for stone in stone_list:
        # print(stone)
        if stone in stone_cache:
            to_ret.extend(stone_cache[stone])

        elif stone == "0":
            stone_cache[stone] = ["1"]
            to_ret.append("1")

        elif len(stone) % 2 == 0:
            left, right = split_stone(stone)
            stone_cache[stone] = [left, right]
            to_ret.append(left)
            to_ret.append(right)
        else:
            to_app = str(int(stone) * 2024)
            stone_cache[stone] = [to_app]
            to_ret.append(to_app)
    return to_ret


def get_five_cache(stone):
    stone_cache[stone] = {"steps": {}}
    stones = [stone]
    for i in range(1, 6):
        stones = blink(stones)
        stone_cache[stone]["steps"][i] = stones
    # stone_cache[stone] = stones
    return stones


if __name__ == "__main__":
    from pprint import pprint

    total = 0
    # start_stones = "5688".split()
    start_stones = "5688 62084 2 3248809 179 79 0 172169".split()
    cache_counts = {}
    # stone = "5688"
    for stone in start_stones:
        _stones = [stone]
        for i in range(38):
            _stones = blink(_stones, i)
        # cache_counts[stone] = len(_stones)
        for s in set(_stones):
            if s in cache_counts:
                continue
            stones = [s]
            for i in range(37):
                stones = blink(stones, i)
            cache_counts[s] = len(stones)
            print(f"finished {s}")
        with open("something.json", "w+") as f:
            f.write(json.dumps(stone_cache))
        for s in _stones:
            total += cache_counts[s]
        pprint(cache_counts)
        print(total)

