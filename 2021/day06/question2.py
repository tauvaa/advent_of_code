import os


def get_data():

    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read().strip()
        data = data.split(",")
        data = list(map(int, data))
    return data


class Fish:
    def __init__(self, inital_timer):
        self.internal_time = inital_timer

    def reproduce_on(self, current_day):
        first_repo = current_day + self.internal_time


class School:
    def __init__(self):
        self.current_day = 0
        self.max_days = 500
        self.repo_days = {i: 0 for i in range(self.max_days)}
        self.num_fish = 0

    def add_fish(self, fish, num_to_add=1):
        self.num_fish += num_to_add
        # print(self.num_fish)
        repo_day = self.current_day + fish.internal_time
        while repo_day < self.max_days:
            self.repo_days[repo_day] += num_to_add
            repo_day += 7

    def pass_day(self):
        repo_num = self.repo_days[self.current_day]
        self.add_fish(Fish(9), repo_num)
        self.current_day += 1


if __name__ == "__main__":
    data = get_data()
    school = School()
    for d in data:
        school.add_fish(Fish(d))
    for i in range(256):
        # print(f"day: {i}")
        school.pass_day()
        # print(school.num_fish)
    #print(school.repo_days)
    print(school.num_fish)
