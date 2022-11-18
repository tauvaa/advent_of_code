import os

with open(os.path.join(os.path.dirname(__file__), "data/data")) as f:
    data = [list(x.strip().split()) for x in f]

data = [[x[0], int(x[1])] for x in data]
hord_pos, vert_pos, aim_pos = 0, 0, 0

for d in data:
    if d[0] == "forward":
        hord_pos += d[1]
        vert_pos += aim_pos * d[1]
    elif d[0] == "up":
        aim_pos -= d[1]
    elif d[0] == "down":
        aim_pos += d[1]
print(hord_pos * vert_pos)
