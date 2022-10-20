# import random
# print([random.randint(0, 10)] * 2)
# a = [[0] * 3] * 3
# a[0][1] = 333
# # for index, row in enumerate(a):
# #     a[index] = row.copy()
# a = [row.copy() for row in a]
# a[0][2] = 444
# print(a)

grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

a = [value for row in grid for value in row]
print(a)