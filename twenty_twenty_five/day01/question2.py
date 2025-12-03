def get_data():
    with open("data.txt") as f:
        data = [l.strip() for l in f]
    return data


class PadLock:
    def __init__(self) -> None:
        self.start_point = 50
        self.clicks = 0

    def turn_left(self, num):
        for i in range(num):
            self.start_point -= 1
            if self.start_point == 0:
                self.clicks += 1
            self.start_point %= 100

    def turn_right(self, num):
        for i in range(num):
            self.start_point += 1
            if self.start_point == 100:
                self.start_point = 0
                self.clicks += 1


if __name__ == "__main__":
    data = get_data()
    pl = PadLock()
    # pl.turn_left(1000)
    # print(pl.clicks)
    # print(pl.start_point)
    for d in data:
        direction = d[0]
        amount = d[1:]
        amount = int(amount)
        if direction == "R":
            pl.turn_right(amount)
        else:
            pl.turn_left(amount)
        # print(pl.start_point)
    print(pl.clicks)
