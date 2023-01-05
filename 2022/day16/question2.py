import heapq
import os
import re


def get_data():
    """Valve NQ has flow rate=0; tunnels lead to valves SU, XD"""
    m = re.compile(r"Valve (\w+).*rate=(\d+).*valves? (.+)")
    with open(os.path.join(os.path.dirname(__file__), "data", "data2")) as f:
        data = [x.strip() for x in f]
    to_ret = []
    for d in data:
        label, rate, leads = m.match(d).groups()
        leads = leads.split(", ")
        rate = int(rate)
        to_ret.append((label, rate, leads))

    return {d[0]: {"rate": d[1], "leads": d[2]} for d in to_ret}


def find_paths(edges, start_point):
    qu = [(0, start_point)]
    all_paths = {start_point: 0}
    while qu:
        cost, point = heapq.heappop(qu)
        for v in edges[point]["leads"]:
            if v not in all_paths:

                all_paths[v] = cost + 1
                heapq.heappush(qu, (cost + 1, v))
            all_paths[v] = min(cost + 1, all_paths[v])

    return all_paths


if __name__ == "__main__":
    data = get_data()

    # paths = find_paths(data, "AA")
    print({x: find_paths(data, x) for x in data})
