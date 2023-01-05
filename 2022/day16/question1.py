import os
from typing import List


def get_valve_data(valvestring):
    valve_label = valvestring.split()[1]
    rate, leads = valvestring.split(";")
    rate = int(rate.split("=")[1])
    valves = leads.split("valve")[1]
    valves = valves[2:] if valves.startswith("s") else valves.strip()
    vavles = valves.replace(" ", "")
    valves = valves.split(",")
    valves = [v.strip() for v in valves]
    return [valve_label, rate, valves]


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = tuple(get_valve_data(l.strip()) for l in f)

    return data


class Valve:
    def __init__(self, valve_name, flow_rate, leads):
        self.valve_name = valve_name
        self.flow_rate = flow_rate
        self.leads = leads


class ValveManager:
    def __init__(self, valves: List[Valve]):
        self.valves = valves

    def get_valve(self, valve_label):
        for v in self.valves:
            if v.valve_name == valve_label:
                return v


def get_valve_paths(current_valve, valvemanger, target, path):
    to_ret = []

    def walk_path(current_valve, valvemanger, target, path):
        if current_valve.valve_name in path:
            return
        if current_valve.valve_name == target:

            to_ret.append(path + [target])
        else:
            for v in current_valve.leads:
                walk_path(
                    valvemanger.get_valve(v),
                    valvemanger,
                    target,
                    path=path + [current_valve.valve_name],
                )

    walk_path(current_valve, valvemanger, target, path)
    return to_ret


def get_min_path(current_valve, valvemanger, target):
    min_path = None

    for p in get_valve_paths(current_valve, valvemanger, target, []):
        if min_path is None:
            min_path = p
        else:
            if len(p) < len(min_path):
                min_path = p
    return min_path


def get_distances(valve, valvemanger):
    to_ret = {
        v.valve_name: len(get_min_path(valve, valvemanger, v.valve_name)) - 1
        for v in valvemanger.valves
        if v.flow_rate
    }
    return to_ret


def all_distances(valvemanager: ValveManager):
    to_ret = {}
    for v in valvemanager.valves:
        if v.flow_rate or v.valve_name == "AA":
            to_ret[v.valve_name] = get_distances(v, valvemanager)
    return to_ret


def get_all_paths(current_node, all_nodes, time_, work_nodes):
    all_paths = []

    def walk_path(current_node, all_nodes, time_, path, work_nodes):
        # print(time_)
        if len(work_nodes) == 1:
            all_paths.append(path + [current_node])
        for node in work_nodes:
            if node == current_node:
                continue
            cost = all_nodes[current_node][node] + 1
            if cost < time_:
                walk_path(
                    node,
                    all_nodes,
                    time_ - cost,
                    path + [current_node],
                    work_nodes - {current_node},
                )
            else:
                all_paths.append(path + [current_node])

    walk_path(current_node, all_nodes, time_, [], work_nodes)
    return all_paths


def execute_path(path, distances, valvemanager, timer=30):
    total = 0
    for i in range(len(path) - 1):
        current = valvemanager.get_valve(path[i])
        timer -= 1 if current.flow_rate else 0
        next_ = valvemanager.get_valve(path[i + 1])
        total += (timer) * current.flow_rate
        timer -= distances[current.valve_name][next_.valve_name]
    total += (timer - 1) * next_.flow_rate
    return total


if __name__ == "__main__":
    data = get_data()
    valves = [Valve(*d) for d in data]

    vm = ValveManager(valves)
    work_nodes = {v.valve_name for v in vm.valves if v.flow_rate}
    current_valve = vm.get_valve("AA")
    distances = all_distances(vm)
    paths = get_all_paths("AA", distances, 30, work_nodes)
    path_values = list(
        map(
            lambda x: execute_path(x, distances=distances, valvemanager=vm),
            paths,
        )
    )
    x = ["AA", "DD", "BB", "JJ", "HH", "EE", "CC"]
    pv = max(path_values)
    print(pv, "here")
