import os


def get_data():
    with open("data.txt") as f:
        data = [line.strip() for line in f]
    return data


def get_highest_number(array, start_point, end_point):
    max_num = array[start_point]
    max_index = start_point
    for i in range(start_point, len(array) - end_point):
        if array[i] > max_num:
            max_num = array[i]
            max_index = i
    return max_index, max_num

def get_largest_nums(datarow):
    nums = []
    current_index = 0
    end_point = 0
    for i in range(12):
        current_index, num = get_highest_number(d, current_index, 11 - i)
        current_index += 1
        nums.append(num)
    return nums

if __name__ == "__main__":
    data = get_data()
    data = [[int(k) for k in line] for line in data]
    all_nums = []
    total = 0
    for d in data:
        s = ""
        x = get_largest_nums(d)
        # print(x)
        # print(len(x))
        for k in x:
            s += str(k)


        all_nums.append(int(s))
    
print(sum(all_nums))
