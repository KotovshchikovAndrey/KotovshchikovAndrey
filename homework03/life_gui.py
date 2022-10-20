import pygame
import typing as tp
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        cell_size: int,
        speed: int = 10
    ) -> None:
        super().__init__(life)

        self.speed = speed
        # Размер квадрата
        self.cell_size = cell_size
        # Динамическая генерация размера поля в зависимости от размера 1 клетки и мощности матрицы
        self.width, self.height = \
            self.life.cell_width * self.cell_size, self.life.cell_height * self.cell_size

        # Создание нового окна
        self.screen = pygame.display.set_mode(
            (self.width, self.height))

        # Цвета, в которые могут окрашиваться клетки
        self._rect_colors = {
            'alive_color': pygame.Color('green'),
            'dead_color': pygame.Color('white'),
        }

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                "black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                "black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row_index in range(self.life.cell_height):
            for col_index in range(self.life.cell_width):
                rect_value = self.life.curr_generation[row_index][col_index]
                color = self._rect_colors['dead_color'] if not rect_value else self._rect_colors['alive_color']

                pygame.draw.rect(
                    surface=self.screen,
                    color=color,
                    rect=(row_index * self.cell_size, col_index * self.cell_size,
                          self.cell_size, self.cell_size)
                )


if __name__ == '__main__':
    game = GameOfLife(
        size=(20, 20),
        randomize=True,
        max_generations=100
    )
    gui = GUI(
        life=game,
        cell_size=32
    )
    gui.run()
