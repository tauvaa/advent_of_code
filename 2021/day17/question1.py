import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:

        data = f.read().strip()

    data = data.split(":")[1]
    data = [x.strip().split("=")[1] for x in data.split(",")]
    data = [x.split("..") for x in data]
    data = [[int(x) for x in y] for y in data]
    return data


class Prob:
    def __init__(self, initial_velocity, target_area):
        self.position = [0, 0]

        self.xvel, self.yvel = initial_velocity
        self.target_x, self.target_y = target_area

    def check_inside(self):
        x, y = self.position
        if (
            self.target_x[0] <= x <= self.target_x[1]
            and self.target_y[0] <= y <= self.target_y[1]
        ):
            return True
        return False

    def check_still_valid(self):
        if self.target_x[1] < self.position[0]:
            return False
        if self.target_y[1] > self.position[1]:
            return False
        return True

    def take_step(self):
        self.position[0] += self.xvel
        self.position[1] += self.yvel
        xchange = 0
        if self.xvel < 0:
            xchange = 1
        if self.xvel > 0:
            xchange = -1
        self.xvel += xchange
        self.yvel -= 1

    def run_prob(self):
        max_y = 0

        while self.check_still_valid():
            self.take_step()
            if max_y < self.position[1]:
                max_y = self.position[1]
            if self.check_inside():
                return max_y
        return -1


if __name__ == "__main__":

    data = get_data()
    num_to_check = 200
    to_check = [(x, y) for x in range(num_to_check) for y in range(num_to_check)]
    all_probs = []
    for k in to_check:
        prob = Prob(k, data)
        all_probs.append((prob.run_prob(), k))
    all_probs.sort(reverse=True)
    print(all_probs[0:10])
    # prob = Prob((7, 2), data)

    # for i in range(10):
    #     prob.take_set()
    #     print(prob.position, prob.check_inside())
