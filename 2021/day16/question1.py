HEXCONVER = """
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
""".strip().split(
    "\n"
)


HEXCONVER = list(map(lambda x: x.split(" = "), HEXCONVER))
HEXCONVER = {x[0]: x[1] for x in HEXCONVER}
print(HEXCONVER)
len_counter = 0


def convert_hex(hexstring):
    to_ret = ""
    for h in hexstring:
        to_ret += HEXCONVER[h]
    return to_ret


class Solver:
    def __init__(self, hexstring):
        self.bstring = convert_hex(hexstring)
        self.chars_used = None
        self.total_length = None
        self.packet_values = []
        self.type_id = None

    def convert_to_bin(self, instring):
        return int(instring, 2)

    def move_string(self, num_char):
        # print(self.chars_used)
        if self.chars_used is not None:
            self.chars_used += num_char

        to_ret = self.bstring[0:num_char]

        self.bstring = self.bstring[num_char:]
        return to_ret

    def literal(self):
        literal_string = ""
        while True:
            to_add = self.move_string(5)

            literal_string += to_add[1:]
            if to_add[0] == "0":
                break
        return literal_string

    def operation(self):
        length_id = self.move_string(1)
        if length_id == "0":
            string_length = 15
            total_length = self.convert_to_bin(self.move_string(string_length))
            self.chars_used = self.chars_used or 0
            chars_used = self.chars_used
            while self.chars_used - chars_used < total_length:
                self.parse_string()
        else:
            string_length = 11
            total_length = self.convert_to_bin(self.move_string(string_length))
            for i in range(total_length):
                self.parse_string()

    def parse_string(self):
        
        version = self.move_string(3)
        type_ = self.convert_to_bin(self.move_string(3))
        if self.type_id is None:
            self.type_id = int(type_)
        iversion = int(self.convert_to_bin(version))
        if type_ == 4:
            print("literal")
            x = self.literal()
            self.packet_values.append(self.convert_to_bin(x))
        else:
            print("operation")
            self.operation()

    def run(self):
        self.parse_string()
        print(self.packet_values)
        print(self.type_id)


if __name__ == "__main__":
    import os

    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = f.read().strip()

    hexstring = "9C0141080250320F1802104A08"
    solution = Solver(hexstring)
    solution.run()
