def get_data():
    with open("data.txt") as f:
        data = [l.strip() for l in f]
    return data
start = 50
zero_counter = 0
for d in get_data():
    num = int(d[1:])
    if d.startswith("L"):
        start -= num
    else:
        start += num
    start %= 100
    if start == 0:
        zero_counter +=1
print(start)

print(zero_counter)
