import pathlib
import random
import typing as tp

from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
        cell_size: int = 10,
    ) -> None:
        # Размер клеточного поля
        self.width, self.height = size
        # Размер квадрата
        self.cell_size = cell_size

        # Количество ячеек по вертикали и горизонтали
        self.cell_width, self.cell_height = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """Создание списка клеток"""
        if not randomize:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        return [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Получение списка соседних клеток.
        """
        row_position, col_position = cell

        # Все возможные соседние позиции
        neighbours_positions_tuple = (
            (row_position, col_position - 1),
            (row_position - 1, col_position),
            (row_position, col_position + 1),
            (row_position + 1, col_position),
            (row_position - 1, col_position - 1),
            (row_position - 1, col_position + 1),
            (row_position + 1, col_position - 1),
            (row_position + 1, col_position + 1),
        )

        neighbours_list = []
        for row_index, col_index in neighbours_positions_tuple:
            # Если координаты позиции отрицательные => такой позиции не существует
            if row_index < 0 or col_index < 0:
                continue

            try:
                neighbour_cell = self.curr_generation[row_index][col_index]
            except IndexError:
                continue
            else:
                neighbours_list.append(neighbour_cell)

        return neighbours_list

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = [row.copy() for row in self.curr_generation]
        for row_index in range(self.cell_height):
            for col_index in range(self.cell_width):
                # Получаем список из соседей каждой клетки и количество живых клеток
                neighbours_list = self.get_neighbours((row_index, col_index))
                alive_neighbours_count = sum(neighbours_list)

                # Если клетка мертва и количество живых соседей == 3, делаем ее живой
                #
                # Если же клетка жива и количество живых соседий от 2 до 3, делаем ее мертвой
                if (not self.curr_generation[row_index][col_index]) and (alive_neighbours_count == 3):
                    new_grid[row_index][col_index] = 1
                elif (self.curr_generation[row_index][col_index]) and (alive_neighbours_count not in (2, 3)):
                    new_grid[row_index][col_index] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.curr_generation = \
            self.curr_generation, self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        pass
