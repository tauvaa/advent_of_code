import os

tdata = [
    607,
    618,
    618,
    617,
    647,
    716,
    769,
    792,
]
print(os.listdir())
with open(os.path.join(os.path.dirname(__file__), "data/data")) as f:
    data = [int(l.strip()) for l in f]
three_groups = []

ind = 0

while ind <= len(data) - 3:
    three_groups.append(sum(data[ind : ind + 3]))
    ind += 1

inc_counter = 0
for k in range(len(three_groups) - 1):
    if three_groups[k] < three_groups[k + 1]:
        inc_counter += 1
print(inc_counter)
