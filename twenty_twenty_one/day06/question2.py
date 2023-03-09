import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = list(map(int, f.read().strip().split(",")))
    return data


class FishSchool:
    def __init__(self, initial_conditions) -> None:
        self.current_day = 0
        self.spawn_days = {}
        self.num_fish = len(initial_conditions)
        for day in initial_conditions:
            if day not in self.spawn_days:
                self.spawn_days[day] = 0

            self.spawn_days[day] += 1

    def move_day(self):
        if self.current_day in self.spawn_days:
            num_new_fish = self.spawn_days[self.current_day]
            self.num_fish += num_new_fish
            new_fish_days, old_fish_days = 9, 7

            if (self.current_day + old_fish_days) not in self.spawn_days:
                self.spawn_days[self.current_day + old_fish_days] = 0
            self.spawn_days[self.current_day + old_fish_days] += num_new_fish

            if (self.current_day + new_fish_days) not in self.spawn_days:
                self.spawn_days[self.current_day + new_fish_days] = 0
            self.spawn_days[self.current_day + new_fish_days] += num_new_fish
        self.current_day += 1


if __name__ == "__main__":
    data = get_data()
    fishschool = FishSchool(data)
    for _ in range(256):
        fishschool.move_day()
        sd = fishschool.spawn_days.copy()
        sd = {
            k - fishschool.current_day: v
            for k, v in sd.items()
            if k >= fishschool.current_day
        }
    print(fishschool.num_fish)
