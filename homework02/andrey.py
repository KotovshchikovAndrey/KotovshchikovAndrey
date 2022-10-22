# # # a = {num for num in range(1, 10)}
# # # b = {num for num in range(3, 5)}
# import typing as tp
# from sudoku import find_empty_positions, find_possible_values, read_sudoku
# # # print(a - b)

# # # def test():
# # #     a = 1
# # #     def t():
# # #         nonlocal a
# # #         a = 2
# # #         print(a)
    
# # #     t()
# # #     print(a)

# # # test()
# # a = [1, 2, 3]
# # b = a.copy()
# # c = b.copy()
# # b.append(0)
# # print(c)

# def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
#     """ Решение пазла, заданного в grid """
#     """ Как решать Судоку?
#         1. Найти свободную позицию
#         2. Найти все возможные значения, которые могут находиться на этой позиции
#         3. Для каждого возможного значения:
#             3.1. Поместить это значение на эту позицию
#             3.2. Продолжить решать оставшуюся часть пазла

#     >>> grid = read_sudoku('puzzle1.txt')
#     >>> solve(grid)
#     [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
#     """
#     solving_grid = None
#     def search(local_grid: tp.List[tp.List[str]]):
#         nonlocal solving_grid

#         empty_positions = find_empty_positions(local_grid)
#         if empty_positions is not None:
#             possible_values_set = find_possible_values(local_grid, empty_positions)
#             if not possible_values_set:
#                  return
            
#             row_empty_position, col_empty_position = empty_positions
#             for values in possible_values_set:
#                 local_grid[row_empty_position][col_empty_position] = values
#                 search(local_grid)
#                 local_grid[row_empty_position][col_empty_position] = '.'
#         else:
#             solving_grid = [row.copy() for row in local_grid]

#     search(grid.copy())
#     return solving_grid

# if __name__ == '__main__':
#     print(solve(read_sudoku('puzzle1.txt')))

print(list(zip([1, 2, 3], [1, 2, 4])))