import os


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [line.strip() for line in f]
    data = [x.split("-") for x in data]
    tdata = []
    for d in data:
        if d[1] == "start":
            d.reverse()
        if d[0] == "end":
            d.reverse()
        tdata.append(d)
    data = tdata
    return data


def check_multi_cave(path):
    lower_caves = list(filter(lambda x: not check_upper(x), path))
    all_chars = {}
    for s in lower_caves:
        if s in all_chars:
            all_chars[s] += 1
        else:
            all_chars[s] = 1
    if max(all_chars.values()) > 2:
        return True
    if len(list(filter(lambda x: x > 1, all_chars.values()))) > 1:
        return True
    return False


def main(starting_points, all_routes):

    complete_paths = []

    def get_paths(inpath, all_routes):
        all_routes = [x for x in all_routes if "start" not in x]
        all_paths = []
        end_path = inpath[-1]
        for r in all_routes:
            if end_path == r[0]:
                total_path = inpath + [r[1]]
                all_paths.append(total_path)
            elif end_path == r[1]:
                total_path = inpath + [r[0]]
                all_paths.append(total_path)
        for p in all_paths:
            if p[-1] == "end":
                complete_paths.append(p)
            else:
                if not check_multi_cave(p):
                    get_paths(p, all_routes)

    for p in starting_points:
        get_paths(p, all_routes)
    return complete_paths


def check_upper(instring):
    return instring.upper() == instring


if __name__ == "__main__":
    data = get_data()
    start_points = [x for x in data if "start" in x]
    # print(start_points)
    complete_paths = main(start_points, data)

    # get_paths("start-A".split("-"), data)
    # get_paths("start-b".split("-"), data)
    print(len(complete_paths))
