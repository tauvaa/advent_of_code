import json
import itertools
import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [line.strip() for line in f]
    return data


class SnailNumber:
    def __init__(self, number):
        self.number = number

    def reduce(self):
        while self._reduce(split=False):
            # print("reducing")
            pass
        while self._reduce(split=True):
            # print("reducing")
            pass

    def check_close(self, start_point):
        current = start_point
        while True:
            current += 1

            if self.number[current] == "[":
                return False
            if self.number[current] == "]":
                return [start_point, current + 1]

    def _reduce(self, split=False):
        bracket_depth = 0
        start_point = None
        digit_start_point = None
        digit_end_point = None

        for idx, char in enumerate(self.number):

            if char == "[":
                bracket_depth += 1
                if bracket_depth > 4:
                    cond = self.check_close(idx)
                    if cond:
                        start_point, end_point = cond
                        self.explode(start_point, end_point)
                        return True

            if char == "]":
                bracket_depth -= 1
            if split:
                if char.isdigit():
                    if digit_start_point is None:
                        digit_start_point = idx
                    digit_end_point = idx + 1
                else:
                    if digit_start_point is not None:
                        if digit_end_point - digit_start_point > 1:
                            self.split(digit_start_point, digit_end_point)
                            return True
                    digit_start_point = None

    def get_right_number(self, start_point):
        current_point = start_point
        while True:
            current_point += 1
            if not self.number[current_point].isdigit():
                return start_point + 1, current_point

    def get_left_number(self, start_point):
        current_point = start_point
        while True:
            current_point -= 1
            if not self.number[current_point].isdigit():
                return current_point + 1, start_point

    def remove_spaces(self):
        self.number = self.number.replace(" ", "")

    def get_regular_right(self, start_point):
        for i in range(start_point, len(self.number)):
            if self.number[i].isdigit():
                counter = 0
                while self.number[i + counter].isdigit():
                    counter += 1

                return [i, i + counter]

    def get_regular_left(self, start_point):
        """
        don't need to consider multi digit numbers because they would split
        first"""
        for i in range(start_point, 0, -1):
            if self.number[i].isdigit():
                counter = 0
                while self.number[i - counter].isdigit():
                    counter += 1
                return [i - counter + 1, i + 1]

    def split(self, start_point, end_point):
        # print("spliting")
        left_num = self.number[0:start_point]

        right_num = self.number[end_point:]
        regnum = self.number[start_point:end_point]
        regnum = int(regnum)
        lowerval = int(regnum / 2)
        upperval = lowerval
        if lowerval + upperval != regnum:
            upperval += 1
        new_list = [lowerval, upperval]
        new_list = str(new_list)
        self.number = left_num + new_list + right_num
        self.remove_spaces()

    def explode(self, start_point, end_point):
        # print("exploding")
        explode_list = self.number[start_point:end_point]
        innerlist = eval(explode_list)
        right = self.get_regular_right(end_point - 1)
        if right is not None:
            x, y = right
            innerlist = eval(explode_list)
            new_right = str(int(self.number[x:y]) + innerlist[1])
            self.number = self.number[0:x] + new_right + self.number[y:]
        left = self.get_regular_left(start_point)
        if left is not None:
            old_left = int(self.number[left[0] : left[1]])
            new_left = str(old_left + innerlist[0])
            if int(new_left) > 9 and old_left < 10:

                start_point += 1
                end_point += 1
            self.number = (
                self.number[0 : left[0]] + new_left + self.number[left[1] :]
            )

        self.number = self.number[0:start_point] + "0" + self.number[end_point:]
        self.remove_spaces()

    def add_number(self, to_add):
        to_add = json.loads(to_add)
        num = json.loads(self.number)

        self.number = str([num, to_add])
        self.remove_spaces()

    def is_pair(self, start_point):
        counter = 0
        while True:
            counter += 1
            if self.number[start_point + counter] == "[":
                return False
            if self.number[start_point + counter] == "]":
                return [start_point, start_point + counter + 1]

    def combine_pair(self):
        for i, char in enumerate(self.number):
            if char == "[":
                pair = self.is_pair(i)
                if pair:
                    num_left = self.number[0 : pair[0]]
                    num_right = self.number[pair[1] :]
                    mag = self.number[pair[0] : pair[1]]
                    mag = json.loads(mag)
                    if len(mag) == 1:
                        return
                    mag = str(3 * mag[0] + 2 * mag[1])
                    self.number = num_left + mag + num_right
                    return True
    def get_manatude(self):
        while self.combine_pair():
            pass
        return int(self.number)

if __name__ == "__main__":
    data = get_data()
    allsets = itertools.permutations(data, 2)
    counter = 0
    max_num = 0
    for s in allsets:
        counter += 1
        counter +=1
        sn = SnailNumber(s[0])
        sn.add_number(s[1])
        sn.reduce()
        max_num = max(int(sn.get_manatude()), max_num)
        if counter %100:
            print(f"counter: {counter}, max value: {max_num}")
    print(max_num)

    # number = data.pop(0)
    # sn = SnailNumber(number)
    # for d in data:
    #     sn.add_number(d)
    #     sn.reduce()
    # num = sn.number
    # while sn.combine_pair():
    #     print("pairing")
    # # print(sn.number)
    # # for d in data:
    # #     sn.add_number(d)
    # #     sn.reduce()
    # print(sn.number)
    # print(num)
