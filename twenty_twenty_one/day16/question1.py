import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip()
    return data


def convert_hex(hexnum):
    converter = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    to_ret = ""
    for ch in hexnum:
        to_ret += converter[ch]
    return to_ret


class PacketManager:
    def __init__(self, bstring) -> None:
        self.binstring = bstring
        self.version = int(self.binstring[0:3], 2)
        self.type_id = int(self.binstring[3:6], 2)
        self.current_position = 6
        self.versions = []

    def get_literal(self):
        return int(self.get_bin_literal(self.binstring[6:]), 2)

    def get_bin_literal(self, bstring):
        to_ret = ""
        current_place = 0

        while True:
            next_place = current_place + 5
            self.current_position += 5
            to_add = bstring[current_place:next_place]
            to_ret += to_add[1:]

            if to_add.startswith("0"):
                break
            current_place = next_place
        return to_ret

    def get_operator(self):
        self.len_id = self.binstring[self.current_position]
        self.current_position += 1
        sub_length = 15 if self.len_id == "0" else 11

        length = self.binstring[
            self.current_position : self.current_position + sub_length
        ]

        self.current_position += sub_length
        length = int(length, 2)
        if self.len_id == "1":
            return length

        return self.binstring[
            self.current_position : self.current_position + length
        ]

    def run(self):
        ops = []
        if self.type_id == 4:
            ops.append(self.get_literal())
        else:
            op = self.get_operator()
            if self.len_id == "0":
                while len(op) > 0:

                    mp = PacketManager(op)
                    versions, toapp = mp.run()
                    self.current_position += mp.current_position
                    self.versions.append(mp.version)

                    if toapp:
                        ops += toapp
                    self.versions += versions
                    op = op[mp.current_position :]
            else:
                for i in range(int(op)):
                    bstring = self.binstring[self.current_position :]
                    mp = PacketManager(bstring)
                    self.versions.append(mp.version)
                    versions, toapp = mp.run()
                    if toapp:
                        ops += toapp
                    self.versions += versions
                    self.current_position += mp.current_position
        return self.versions, ops


if __name__ == "__main__":

    data = get_data()
    pm = PacketManager(convert_hex(data))
    pm.run()
    pm.versions.append(pm.version)
    print(sum(pm.versions))
