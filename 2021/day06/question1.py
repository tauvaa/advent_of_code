import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip()
        data = data.split(",")
        data = list(map(int, data))
    return data


class Fish:
    def __init__(self, inital_timer):
        self.internal_time = inital_timer

    def pass_day(self):
        self.internal_time -= 1


class School:
    def __init__(self):
        self.school = []

    def add_fish(self, fish):
        self.school.append(fish)

    def pass_day(self):
        to_add = 0
        for fish in self.school:
            if fish.internal_time == 0:
                to_add += 1
                fish.internal_time = 6
            else:
                fish.pass_day()
        self.school += [Fish(8) for _ in range(to_add)]

    def print_school(self):
        print_string = ",".join([str(x.internal_time) for x in self.school])
        print(print_string)

    def get_school_size(self):
        print(len(self.school))


if __name__ == "__main__":
    data = get_data()
    school = School()
    for d in data:
        school.add_fish(Fish(d))
    for i in range(150):
        
        school.pass_day()
        # school.print_school()

    school.get_school_size()
