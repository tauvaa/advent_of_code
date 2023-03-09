import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data1")) as f:
        data = [line.strip().split("-") for line in f]
    for i, d in enumerate(data):
        if d[1] == "start":
            data[i] = [d[1], d[0]]
    return data


def get_next_point(current_point, linker):
    if linker[0] == current_point:
        return linker[1]
    return linker[0]


def is_caps(instring):
    if instring.upper() == instring:
        return True
    return False


def get_paths(data):
    """
    Have a structure like:
        [current path, visitied points]
    """
    final_paths = []
    paths = []
    for d in data:
        if "start" in d:
            paths.append([d, set(["start", get_next_point("start", d)])])

    while paths:
        next_path = paths.pop(0)
        current_place = next_path[0][-1]
        if current_place == "end":
            final_paths.append(next_path[0])
            continue
        for d in data:
            if current_place in d:

                next_step = get_next_point(current_place, d)
                if is_caps(next_step) or next_step not in next_path[1]:
                    visited_paths = next_path[1].copy()
                    visited_paths.add(next_step)
                    paths.append([next_path[0] + [next_step], visited_paths])
    return final_paths


if __name__ == "__main__":
    data = get_data()
    paths = get_paths(data)
    print(len(paths))
