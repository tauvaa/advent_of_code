import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = f.read()
    data = data.split("\n")
    data = list(filter(lambda x: x != "", data))

    return data


class Register:
    def __init__(self):
        self.sprite = 0
        self.register = 1
        self.cycle = 0
        self.cycle_values = []
        self.screen = []
        self.current_row = ""

    def run_cycle(self):
        if self.sprite in [self.register - 1, self.register, self.register + 1]:
            self.current_row += "#"
        else:
            self.current_row += "."

        self.cycle_values.append(self.register)
        self.cycle += 1
        self.sprite += 1
        if self.cycle % 40 == 0:
            self.sprite = 0
            self.screen.append(self.current_row)
            self.current_row = ""

    def execute_instruction(self, instruction):
        instruction = instruction.split()
        if len(instruction) == 1:
            self.run_cycle()
        else:
            instruction, value = instruction

            value = int(value)
            self.run_cycle()
            self.run_cycle()
            self.register += value


if __name__ == "__main__":
    data = get_data()
    reg = Register()
    for inst in data:
        reg.execute_instruction(inst)
    reg.run_cycle()
    for s in reg.screen:
        print(s)

