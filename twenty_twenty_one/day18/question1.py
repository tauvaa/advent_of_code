import json
import re


class SnailNumber:
    def __init__(self, number):
        self.number = number

    def reduce(self):
        bracket_depth = 0
        start_point = None
        for idx, char in enumerate(self.number):
            if char == ",":
                if self.number[idx - 1] == "]":
                    start_point, end_point = self.get_right_number(idx)
                    if end_point - start_point > 1:
                        self.split(start_point, end_point)
                        return True
                if (
                    self.number[idx + 1] == "["
                    and self.number[idx - 1].isdigit()
                ):
                    start_point, end_point = self.get_left_number(idx)

                    if end_point - start_point > 1:
                        print("here")
                        self.split(start_point, end_point)
                        return True
            if char == "[":
                bracket_depth += 1
                if bracket_depth > 4:
                    start_point = idx
            if char == "]":
                bracket_depth -= 1
                if bracket_depth > 3:
                    end_point = idx + 1
                    self.explode(start_point, end_point)
                    return True

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
        for i in range(start_point, len(self.number) - 2):
            if (
                self.number[i] == "]"
                and self.number[i + 1] == ","
                and self.number[i + 2].isdigit()
            ):
                counter = 0
                while self.number[i + 2 + counter].isdigit():
                    counter += 1

                return [i + 2, i + counter + 2]

    def get_regular_left(self, start_point):
        """
        don't need to consider multi digit numbers because they would split
        first"""
        for i in range(start_point, 3, -1):
            if (
                self.number[i] == "["
                and self.number[i - 1] == ","
                and self.number[i - 2].isdigit()
                and self.number[i - 3] == "["
            ):
                return i - 2

    def split(self, start_point, end_point):
        print("spliting")
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
        print("exploding")
        explode_list = self.number[start_point:end_point]
        innerlist = eval(explode_list)
        right = self.get_regular_right(end_point - 1)
        if right:
            x, y = right
            innerlist = eval(explode_list)
            new_right = str(int(self.number[x:y]) + innerlist[1])
            self.number = self.number[0:x] + new_right + self.number[y:]
        left = self.get_regular_left(end_point)
        if left:
            new_left = str(int(self.number[left]) + innerlist[0])
            self.number = (
                self.number[0:left] + new_left + self.number[left + 1 :]
            )
        self.number = self.number[0:start_point] + "0" + self.number[end_point:]
        self.remove_spaces()

    def add_number(self, to_add):
        to_add = json.loads(to_add)
        num = json.loads(self.number)

        self.number = str([num, to_add])
        self.remove_spaces()


if __name__ == "__main__":
    number = "[[[[10,[9,8],1],2],3],4]"
    # number = "[7,[6,[5,[4,[3,2]]]]]"
    # number = "[[6,[5,[4,[3,2]]]],1]"
    number = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    number = "[[[[4,3],4],4],[7,[[8,4],9]]]"
    to_add = "[1,1]"
    sn = SnailNumber(number)
    sn.add_number(to_add)
    while sn.reduce():
        print("reducing")
    print(sn.number)
