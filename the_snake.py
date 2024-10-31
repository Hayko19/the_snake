from random import randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Значение цвета по умолчанию:
COLOR = (255, 255, 255)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Родительский класс."""

    def __init__(self, color=COLOR) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color

    def draw_cell(self, position, color):
        """Отрисовка сегмента с заданной позицией и цветом."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод - заглушка для переопределения."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, snake=None):
        super().__init__(APPLE_COLOR)
        self.occupied = []
        if snake is not None:
            self.randomize_position(snake)
        else:
            self.position = (0, 0)

    def randomize_position(self, snake):
        """Метод для рандомного спавна яблока."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        while self.position in snake.positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Переопределяем метод draw для яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Переопределяем метод draw для змейки."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

        # Затираем последний сегмент, если он существует
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def update_direction(self):
        """Метод обрабатывающий следующее направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Метод отвечающий за движение змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        head_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT

        self.positions.insert(0, (head_x, head_y))

    def reset(self):
        """Метод для сброса положения змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Функция обрабатывающая варианты взаимодействия с пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_UP or event.key == pygame.K_w)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif ((event.key == pygame.K_DOWN or event.key == pygame.K_s)
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif ((event.key == pygame.K_LEFT or event.key == pygame.K_a)
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif ((event.key == pygame.K_RIGHT or event.key == pygame.K_d)
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
        else:
            snake.positions.pop()

    # Проверка столкновения с телом
        for position in snake.positions[1:]:  # Пропускаем голову
            if snake.get_head_position() in snake.positions[1:]:
                snake.reset()  # Сбрасываем игру

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
