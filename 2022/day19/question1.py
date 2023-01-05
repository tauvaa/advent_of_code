import os
import re

import numpy as np


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        match_string = r".*Each (\w+).*costs (.+).*"
        to_ret = []
        to_app = []
        for line in f:

            if line == "\n":
                to_ret.append(to_app)
                to_app = []
            elif line.startswith("Blue"):
                pass

            else:
                to_app.append(line.strip())
        if len(to_app) > 1:
            to_ret.append(to_app)
    temp = to_ret
    to_ret = []
    for d in temp:
        to_app = []
        for k in d:
            m = re.match(match_string, k)
            robot_type, robot_cost = m.groups()
            robot_cost = robot_cost.strip(".")
            to_app.append((robot_type, robot_cost))
        to_ret.append(to_app)
    to_ret = [dict(x) for x in to_ret]

    return to_ret


class Simulation:
    def __init__(
        self,
        instructions,
        ore_per_turn,
        clay_per_turn,
        obsidian_per_turn,
        geode_per_turn,
        num_ore,
        num_clay,
        num_obsidian,
        num_geode,
        time_remaining,
    ) -> None:
        self.all_instructions = instructions
        self.instructions_ore = self.parse_instructions(instructions["ore"])
        self.instructions_clay = self.parse_instructions(instructions["clay"])
        self.instructions_obsidian = self.parse_instructions(
            instructions["obsidian"]
        )
        self.instructions_geode = self.parse_instructions(instructions["geode"])

        self.ore_per_turn = ore_per_turn
        self.clay_per_turn = clay_per_turn
        self.obsidian_per_turn = obsidian_per_turn
        self.geode_per_turn = geode_per_turn

        self.new_sims = []
        self.time_remaining = time_remaining

        self.ore = num_ore
        self.clay = num_clay
        self.obsidian = num_obsidian
        self.geode = num_geode
        self.steps = []

    def take_turn(self):
        self.time_remaining -= 1
        self.ore += self.ore_per_turn
        self.clay += self.clay_per_turn
        self.obsidian += self.obsidian_per_turn
        self.geode += self.geode_per_turn
        ore_dict = {
            "ore": self.ore,
            "clay": self.clay,
            "obsidian": self.obsidian,
            "geode": self.geode,
        }
        if self.time_remaining < 20:
            if self.ore_per_turn + self.clay_per_turn < 2:
                return

        self.steps.append(ore_dict)
        if self.time_remaining > 0:
            if all(ore_dict[k] >= v for k, v in self.instructions_ore.items()):
                self.new_sims.append(
                    self.make_simulation(self.instructions_ore, "ore")
                )

            if all(ore_dict[k] >= v for k, v in self.instructions_clay.items()):
                self.new_sims.append(
                    self.make_simulation(self.instructions_clay, "clay")
                )
            if all(
                ore_dict[k] >= v for k, v in self.instructions_obsidian.items()
            ):
                self.new_sims.append(
                    self.make_simulation(self.instructions_obsidian, "obsidian")
                )
            if all(
                ore_dict[k] >= v for k, v in self.instructions_geode.items()
            ):
                self.new_sims.append(
                    self.make_simulation(self.instructions_geode, "geode")
                )

    def make_simulation(self, oredict, robot_type):
        ore_per_turn = self.ore_per_turn
        clay_per_turn = self.clay_per_turn
        obsidian_per_turn = self.obsidian_per_turn
        geode_per_turn = self.geode_per_turn

        # ore = self.ore + self.ore_per_turn - (oredict.get("ore") or 0)
        ore = self.ore
        if oredict.get("ore"):
            ore -= oredict.get("ore")
        ore += self.ore_per_turn
        clay = self.clay + self.clay_per_turn - (oredict.get("clay") or 0)
        obsidian = (
            self.obsidian
            + self.obsidian_per_turn
            - (oredict.get("obsidian") or 0)
        )
        geode = self.geode + self.geode_per_turn - (oredict.get("geode") or 0)
        if robot_type == "ore":
            ore_per_turn += 1
        if robot_type == "clay":
            clay_per_turn += 1

        if robot_type == "obsidian":
            obsidian_per_turn += 1
        if robot_type == "geode":
            geode_per_turn += 1

        return Simulation(
            instructions=self.all_instructions,
            ore_per_turn=ore_per_turn,
            clay_per_turn=clay_per_turn,
            obsidian_per_turn=obsidian_per_turn,
            geode_per_turn=geode_per_turn,
            num_ore=ore,
            num_clay=clay,
            num_obsidian=obsidian,
            num_geode=geode,
            time_remaining=self.time_remaining - 1,
        )

    def get_ore_dict(self):
        return {
            "ore": self.ore,
            "clay": self.clay,
            "obsidian": self.obsidian,
            "geode": self.geode,
        }

    def run_simulation(self):
        while self.time_remaining > 0:
            self.take_turn()

    def parse_instructions(self, instruction):
        instructions = instruction.split("and")
        to_ret = {}

        for i in instructions:
            i = i.strip()
            num, t = i.split(" ")
            to_ret[t] = int(num)
        return to_ret


if __name__ == "__main__":

    data = get_data()
    print(data)
    simulation = Simulation(
        data[1], 1, 0, 0, 0, 0, 0, 0, num_geode=0, time_remaining=24
    )

    all_sims = [simulation]
    max_g = 0
    while all_sims:
        simulation = all_sims.pop()

        simulation.run_simulation()
        all_sims += simulation.new_sims
        max_g = max(max_g, simulation.geode)
    print(max_g)
