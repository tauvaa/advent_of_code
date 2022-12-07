import os


def get_data():
    print("here")
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [line.strip().split(" ") for line in f]
    return data


def get_choice(invalue):
    if invalue in ("A", "X"):
        return 1, "rock"
    if invalue in ("B", "Y"):
        return 2, "paper"
    if invalue in ("C", "Z"):
        return 3, "scissors"


def make_choice(opponent, outcome):
    if outcome == "X":
        # loss
        if opponent == "rock":
            return "scissors"
        if opponent == "paper":
            return "rock"
        if opponent == "scissors":
            return "paper"

    if outcome == "Y":
        # tie
        if opponent == "rock":
            return "rock"
        if opponent == "paper":
            return "paper"
        if opponent == "scissors":
            return "scissors"
    if outcome == "Z":
        # win
        if opponent == "rock":
            return "paper"
        if opponent == "paper":
            return "scissors"
        if opponent == "scissors":
            return "rock"


def get_outcome(opponent, me):
    if me == "rock":
        if opponent == "paper":
            return 0 + 1
        if opponent == "scissors":
            return 6 + 1
        if opponent == "rock":
            return 3 + 1
    if me == "paper":
        if opponent == "rock":
            return 6 + 2
        if opponent == "paper":
            return 3 + 2
        if opponent == "scissors":
            return 0 + 2
    if me == "scissors":
        if opponent == "rock":
            return 0 + 3
        if opponent == "paper":
            return 6 + 3
        if opponent == "scissors":
            return 3 + 3


def play_game(opponent, outcome):
    _, opponent = get_choice(opponent)
    me = make_choice(opponent, outcome)
    print(opponent, me)
    return get_outcome(opponent, me)


if __name__ == "__main__":
    data = get_data()
    total = 0
    for d in data:
        print(d)
        x = play_game(*d)
        print(x)
        total += x
    print(total)
