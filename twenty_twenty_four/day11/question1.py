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
start_stones = "0 1 10 99 999"
start_stones = start_stones.split(" ")
# start_stones = map(int, start_stones.split(" "))


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


def blink(stone_list):
    to_ret = []
    for stone in stone_list:
        if stone == "0":
            to_ret.append("1")
        elif len(stone) % 2 == 0:
            left, right = split_stone(stone)
            to_ret.append(left)
            to_ret.append(right)
        else:
            to_app = str(int(stone) * 2024)
            to_ret.append(to_app)
    return to_ret


start_stones = "5688 62084 2 3248809 179 79 0 172169".split()
# print(blink(start_stones))
for _ in range(25):
    start_stones = blink(start_stones)
print(len(start_stones))
