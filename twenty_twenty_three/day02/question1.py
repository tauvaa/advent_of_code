import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "day1")) as f:
        data = [line for line in f]
    return data


def get_game_information(line):
    pattern = r"Game (\d+): (.*)"
    m = re.match(pattern, line)
    game_id, game_info = m.groups()
    game_id = int(game_id)
    game_info = [[x.strip() for x in game.split(",")] for game in game_info.split(";")]
    game_info_new = []

    for game in game_info:
        to_app = {}
        for g in game:
            num, color = g.split(" ")
            to_app[color] = int(num)
        game_info_new.append(to_app)
    return game_id, game_info_new


def is_valid_game(red=0, blue=0, green=0):
    redmax, greenmax, bluemax = 12, 13, 14
    return all((red <= redmax, blue <= bluemax, green <= greenmax))


if __name__ == "__main__":
    data = get_data()
    total = 0
    for line in data:
        valid_game = True
        game_id, game_info = get_game_information(line)
        for game in game_info:
            if not is_valid_game(**game):
                valid_game = False
                break
        if valid_game:
            total += game_id
    print(total)
