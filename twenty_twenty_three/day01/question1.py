import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "question1")) as f:
        data = f.read()
    data = data.strip()
    data = data.split("\n")
    return data
def get_digits(line):

    first_digit, second_digit = None, None
    for c in line:
        if c.isdigit():
            if first_digit is None:
                first_digit = c
            else:
                second_digit = c
    second_digit = second_digit or first_digit 
    return int(first_digit + second_digit)
if __name__ == "__main__":
    total = 0
    for line in get_data():
        total += get_digits(line)
    print(total)




