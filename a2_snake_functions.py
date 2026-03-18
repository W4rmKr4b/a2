# Functions for Snake Game

from constants import EMPTY, FOOD, HEAD, SNAKE_BODY


def initial_snake():
    """Returns the starting position of the snake as a list of coordinates."""
    return [(5, 5), (5, 4), (5, 3)]


def move_snake(snake, direction):
    """Moves the snake in the specified direction (up, down, left, right)."""
    head = snake[0]
    if direction == 'up':
        new_head = (head[0] - 1, head[1])
    elif direction == 'down':
        new_head = (head[0] + 1, head[1])
    elif direction == 'left':
        new_head = (head[0], head[1] - 1)
    elif direction == 'right':
        new_head = (head[0], head[1] + 1)
    else:
        raise ValueError("Invalid direction")
    return [new_head] + snake[:-1]


def grow_snake(snake):
    """Adds a segment to the snake's tail."""
    return snake + [snake[-1]]


def check_collision(snake, position):
    """Checks if the snake collides with itself or the walls."""
    if position in snake:
        return True
    head = snake[0]
    if head[0] < 0 or head[0] >= 10 or head[1] < 0 or head[1] >= 10:
        return True
    return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()