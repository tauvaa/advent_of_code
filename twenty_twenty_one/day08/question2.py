import os


def alphabetize(instring):
    to_ret = list(instring)
    to_ret.sort()
    return "".join(to_ret)


def get_data():
    data = []
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        for line in f:
            line = line.split("|")
            line = [x.strip() for x in line]
            line = [x.split() for x in line]

            data.append(line)

    return data


class Numbers:
    def __init__(self, data):
        self.data = data

        self.all_strings = data[0] + data[1]
        self.all_strings = [set(x) for x in self.all_strings]
        self.zero = set()
        self.one = set()
        self.two = set()
        self.three = set()
        self.four = set()
        self.five = set()
        self.six = set()
        self.seven = set()
        self.eight = set()
        self.nine = set()
        self.get_unique()
        self.get_six()
        self.get_nine()
        self.get_zero()
        self.get_five()
        self.get_three()
        self.get_two()

    def get_output(self):
        oput = [set(o) for o in self.data[1]]
        to_ret = ""
        for o in oput:
            if o == self.zero:
                to_ret += "0"
            if o == self.one:
                to_ret += "1"
            if o == self.two:
                to_ret += "2"
            if o == self.three:
                to_ret += "3"
            if o == self.four:
                to_ret += "4"
            if o == self.five:
                to_ret += "5"
            if o == self.six:
                to_ret += "6"
            if o == self.seven:
                to_ret += "7"
            if o == self.eight:
                to_ret += "8"
            if o == self.nine:
                to_ret += "9"
        return to_ret

    def get_unique(self):
        for d in self.all_strings:
            if len(d) == 2:
                self.one = set(d)
            if len(d) == 3:
                self.seven = set(d)
            if len(d) == 4:
                self.four = set(d)
            if len(d) == 7:
                self.eight = set(d)

    def get_two(self):
        five_data = [x for x in self.all_strings if len(x) == 5]
        for s in five_data:
            if s != self.three and s != self.five:
                self.two = s

    def get_three(self):
        five_data = [x for x in self.all_strings if len(x) == 5]
        for s in five_data:
            if (
                s.intersection(self.nine) == s
                and len(s.intersection(self.one)) == 2
            ):
                self.three = s

    def get_five(self):
        five_data = [x for x in self.all_strings if len(x) == 5]
        for s in five_data:
            if (
                s.intersection(self.nine) == s
                and len(s.intersection(self.one)) == 1
            ):

                self.five = s

    def get_six(self):
        six_data = [x for x in self.all_strings if len(x) == 6]
        for s in six_data:
            if len(s.intersection(self.one)) == 1:
                self.six = s

    def get_nine(self):
        six_data = [x for x in self.all_strings if len(x) == 6]
        for s in six_data:
            if len(s.intersection(self.six)) != len(self.six):
                if len(s.intersection(self.six).intersection(self.four)) == 3:
                    self.nine = s

    def get_zero(self):
        six_data = [x for x in self.all_strings if len(x) == 6]
        for s in six_data:
            if s != self.six and s != self.nine:
                self.zero = s


if __name__ == "__main__":
    data = get_data()
    nums = []
    for d in data:
        numbers = Numbers(d)
        nums.append(int(numbers.get_output()))
    print(sum(nums))
