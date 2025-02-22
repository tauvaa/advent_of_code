import os
import re


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "day2")) as f:
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


if __name__ == "__main__":
    data = get_data()
    total = 0
    for line in data:
        game_id, game_info = get_game_information(line)
        min_red, min_green, min_blue = 0, 0, 0
        for game in game_info:
            if min_red < game.get("red", 0):
                min_red = game["red"]

            if min_blue < game.get("blue", 0):
                min_blue = game["blue"]

            if min_green < game.get("green", 0):
                min_green = game["green"]
        total += min_red * min_blue * min_green
    print(total)
