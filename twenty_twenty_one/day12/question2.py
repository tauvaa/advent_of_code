import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
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
    visited_paths = {}
    for d in data:
        for place in d:
            if place not in visited_paths:
                visited_paths[place] = 0
    final_paths = []
    paths = []
    for d in data:
        if "start" in d:
            visited = visited_paths.copy()
            visited["start"] = 1
            visited[get_next_point("start", d)] = 1

            paths.append([d, visited])

    while paths:
        next_path = paths.pop(0)
        current_place = next_path[0][-1]
        if current_place == "end":
            final_paths.append(next_path[0])
            continue
        for d in data:
            if current_place in d:
                next_step = get_next_point(current_place, d)
                if (
                    is_caps(next_step)
                    or (
                        all([x < 2 for x in next_path[1].values()])
                        or next_path[1][next_step] == 0
                    )
                ) and next_step != "start":
                    visited_paths = next_path[1].copy()
                    if not is_caps(next_step):
                        visited_paths[next_step] += 1
                    paths.append([next_path[0] + [next_step], visited_paths])
    return final_paths


if __name__ == "__main__":
    data = get_data()
    paths = get_paths(data)
    print(len(paths))
