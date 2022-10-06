import pathlib
import typing as tp

# размер игрового
FIELD_SIZE = (9, 9)

# размер маленького квадрата
SQUARE_SIZE = (3, 3)

# множество из всех возможных элементов (цифр)
UNIVERSAL_SET = {str(num) for num in range(1, 10)}

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """ Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """ Сгруппировать значения values в список, состоящий из списков по n элементов """
    group_matrix = []
    for i in range(0, len(values), n):
        group_matrix.append(values[i:i+n])

    return group_matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера строки, указанной в pos """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos """
    col = []
    for row in grid:
        col.append(row[pos[1]])

    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos """
    sector_position = (
        pos[0] // SQUARE_SIZE[0],
        pos[1] // SQUARE_SIZE[1]
    )
    # индекс строки, где начинается сектор
    sectror_row_start_position = sector_position[0] * SQUARE_SIZE[0]

    # индекс строки, где заканчивается сектор (не включительно)
    sectror_row_end_position = sectror_row_start_position + SQUARE_SIZE[0]

    # индекс колонки, где начинается сектор
    sector_col_start_position = sector_position[1] * SQUARE_SIZE[1]

    # индекс колонки, где заканчивается сектор (не включительно)
    sector_col_end_position = sector_col_start_position + SQUARE_SIZE[1]

    square_elements_list = []
    for row in grid[sectror_row_start_position:sectror_row_end_position]:
        square_elements_list.extend(row[sector_col_start_position:sector_col_end_position])
    
    return square_elements_list


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле """
    for row_index, row in enumerate(grid):
        if '.' in row:
            return row_index, row.index('.')
    
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """ Вернуть множество возможных значения для указанной позиции """
    row, col = get_row(grid, pos), get_col(grid, pos)
    sector_values = set(get_block(grid, pos))

    free_values_in_sectror = UNIVERSAL_SET - sector_values
    posible_values_set = set()
    for free_element in free_values_in_sectror:
        if any([free_element in row, free_element in col]):
            continue

        posible_values_set.add(free_element)
    
    return posible_values_set


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """

    # перемнная, в которое помещается решение судоку (по умолчанию None)
    solving_grid = None
    def search(local_grid: tp.List[tp.List[str]]) -> None:
        """ Рекурсивная функция для поиска решения """
        nonlocal solving_grid

        empty_positions = find_empty_positions(local_grid)

        # (блок if)
        # проверяем, остались ли еще незаполненные поля
        #
        # (блок else)
        # если пустых полей нет, значит мы нашли решение
        # в переменную solving_grid присваиваем новый объект list
        if empty_positions is not None:
            possible_values_set = find_possible_values(local_grid, empty_positions)

            # если нет вариантов для решения, то дальше не идем
            if not possible_values_set:
                 return
            
            row_empty_position, col_empty_position = empty_positions
            for values in possible_values_set:
                local_grid[row_empty_position][col_empty_position] = values
                search(local_grid)
                local_grid[row_empty_position][col_empty_position] = '.'
        else:
            solving_grid = solving_grid = [row.copy() for row in local_grid]

    search(grid.copy())
    return solving_grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
