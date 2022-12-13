import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read()
    data = data.split("\n")
    data = list(filter(lambda x: x != "", data))

    return data


class Register:
    def __init__(self):
        self.register = 1
        self.cycle = 0
        self.cycle_values = []

    def run_cycle(self):
        self.cycle_values.append(self.register)
        self.cycle += 1

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
    total = 0
    for i in range(20, len(reg.cycle_values), 40):
        print(i)
        print(reg.cycle_values[i - 1])
        total += i * reg.cycle_values[i - 1]
    print(f"total is: {total}")
