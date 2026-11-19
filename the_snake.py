from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_TO_DIRECTION = {
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 30

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка | Выход: Esc | Скорость: +/-')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw_cell(self, position, cell_color, border_color=None):
        """
        Отрисовывает одну ячейку:
        заливка cell_color, контур border_color.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, cell_color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Отрисовка объектов на экране."""
        raise NotImplementedError(
            'Переопределите метод draw, в дочерних классах GameObject'
        )


class Apple(GameObject):
    """Базовый класс объекта яблока."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Перемещает объект в случайную свободную клетку поля."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Базовый класс объекта змейка."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновление координат всех сегментов змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        if direction:
            self.direction = direction

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовывает голову змейки и затирает покинутую клетку."""
        self.draw_cell(self.get_head_position(), self.body_color, BORDER_COLOR)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш. Возвращает False при выходе из игры."""
    global SPEED
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
            if event.key in (pg.K_PLUS, pg.K_KP_PLUS, pg.K_EQUALS):
                SPEED = min(SPEED + 5, 60)
            elif event.key in (pg.K_MINUS, pg.K_KP_MINUS):
                SPEED = max(SPEED - 5, 1)
            else:
                game_object.update_direction(
                    KEY_TO_DIRECTION.get(
                        (game_object.direction, event.key),
                        game_object.direction
                    )
                )
    return True


def main():
    """Запуск игры «Змейка»."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=[snake.get_head_position()])
    occupied_positions = [snake.get_head_position(), apple.position]

    stones = [
        Apple(body_color=STONE_COLOR)
        for _ in range(randint(0, 10))
    ]
    for stone in stones:
        stone.randomize_position(occupied_positions)
        occupied_positions.append(stone.position)

    while True:
        clock.tick(SPEED)
        if not handle_keys(snake):
            break
        snake.move()
        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            occupied_positions = (
                snake.positions[:]
                + [stone.position for stone in stones]
            )
            apple.randomize_position(occupied_positions)
            occupied_positions.append(apple.position)

        elif (head_position in snake.positions[1:]
              or head_position in [stone.position for stone in stones]):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            occupied_positions = snake.positions[:]
            apple.randomize_position(occupied_positions)
            occupied_positions.append(apple.position)

            for stone in stones:
                stone.randomize_position(occupied_positions)
                occupied_positions.append(stone.position)

        apple.draw()
        snake.draw()
        for stone in stones:
            stone.draw_cell(stone.position, stone.body_color)
        pg.display.update()


if __name__ == '__main__':
    main()
