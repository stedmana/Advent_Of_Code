
def find_ans(val_in):
    integer_val = int(val_in)
    floor_3 = integer_val // 3
    sub_2 = floor_3 - 2
    if sub_2 < 0:
        return 0
    return sub_2

# print(find_ans(100756))

sum = 0
with open('./input1.txt') as fp:
    for item in fp:
        sum += find_ans(item)
print('part1: {}'.format(sum))

sum2 = 0
with open('./input1.txt') as fp:
    for item in fp:
        mid_sum = 0
        current_need = find_ans(item)
        while current_need > 0:
            mid_sum += current_need
            current_need = find_ans(current_need)
        sum2 += mid_sum

print('part2: {}'.format(sum2))
