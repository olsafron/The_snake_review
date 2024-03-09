# The_snake
"""Игра змейка.Спринт 2."""
from random import randint
import pygame

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
SPEED = 10
TEXT_COLOR = (255, 255, 255)

pygame.init()


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для обЪектов в игре."""

    def __init__(self, position=None, color=APPLE_COLOR):
        """Инициалзация атрибутов обЪекта."""
        self.position = position
        self.body_color = color

    def draw_one_element(self, position=None, color=None):
        """Отрисовка одного обЪекта на поле."""
        draw_position = position or self.position
        draw_color = color or self.body_color

        rect = pygame.Rect(draw_position,
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, draw_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для отрисовки обЪекта
        на заданном поле.
        Производные классы реализуют этот метод
        для отрисовки своиХ обЪектов на экране.
        """
        raise NotImplementedError("Не трогай!")


class Snake(GameObject):
    """Класс реализующий змейку в игре."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализация начального состояния змейки."""
        super().__init__(
            position=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)], color=color
        )
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Метод отрисовывания змейки на экране."""
        # Отрисовка головы змейки
        head_position = self.get_head_position()
        self.draw_one_element(position=head_position, color=SNAKE_COLOR)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод движения змейки."""
        # Координаты головы это всегда первый элемент.
        head_position_x, head_position_y = self.get_head_position()

        # Направление движения
        dx, dy = self.direction
        # Новая позиция головы.
        new_position_x = (head_position_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_position_y = (head_position_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_position_x, new_position_y)
        self.positions.insert(0, new_head)
        # Если змея сЪела яблоко, удалить конец.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Метод возращения позици головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


class Apple(GameObject):
    """Класс реализующий яблоко."""

    def __init__(self, occupied_positions=set(), color=APPLE_COLOR):
        """Инициализирующий метод класса с учётом занятыХ позиций."""
        super().__init__(color=color)
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установка случайного положения яблока на игровом поле."""
        while True:
            rand_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            rand_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (rand_x, rand_y)
            if position not in occupied_positions:
                return position

    def draw(self, surface):
        """Отрисовка яблока на игровом поле."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit("Вышли из игры")

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция управления игрой."""
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # occupied_positions занятые позиции,т.е. позиция змейки.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Новое яблоко
            apple = Apple(occupied_positions=set(snake.position))
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple = Apple(occupied_positions=set(snake.position))
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
