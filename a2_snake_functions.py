"""CSCA08: Winter 2026 -- Assignment 2: Snake Game

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2026 University of Toronto.
All rights reserved. For use at the University of Toronto only.

Prepared by Yimo Ning, with contributions from Javane Rostampoor,
Akshay Bapat, and the CSCA08 teaching assistant team.

Course Acknowledgement: Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, Anya Tafliovich, Paul Gries,
Andrew Petersen, Purva Gawde, Irene Huang and others.

"""

from constants import (
    DOWN,
    EMPTY,
    FOOD,
    HEAD,
    LEFT,
    RIGHT,
    SNAKE_BODY,
    UP,
)


def make_board(width, height):
        """Return a new board with width columns and height rows.
    The returned board is a nested list of strings filled with the
    character ".". The board uses row-major layout:
    board[y][x] refers to column x in row y.

    The board contains exactly height rows, and each row contains
    exactly width columns.

    If width == 0 or height == 0, return [].

    Preconditions:
    - width >= 0
    - height >= 0

    >>> make_board(3, 2)
    [['.', '.', '.'], ['.', '.', '.']]
    """
    if width == 0 or height == 0:
        return []
    return [["."] * width for _ in range(height)]

# =======Add the rest of functions here=========
# ===================================

def clear_board(board):
    """Mutate board so every position becomes '.'.

    >>> b = [['H', 'F'], ['S', '.']]
    >>> clear_board(b)
    >>> b
    [['.', '.'], ['.', '.']]
    """
    for y in range(len(board)):
        for x in range(len(board[y])):
            board[y][x] = "."


def place_snake_and_food(board, snake, food):
    """Clear board, then place snake and food.

    Snake is [[x, y], ...] where index 0 is head.

    >>> b = make_board(4, 3)
    >>> place_snake_and_food(b, [[1, 1], [0, 1], [0, 2]], [3, 0])
    >>> b
    [['.', '.', '.', 'F'], ['S', 'H', '.', '.'], ['S', '.', '.', '.']]
    """
    clear_board(board)

    if snake:
        head_x, head_y = snake[0]
        board[head_y][head_x] = "H"
        for x, y in snake[1:]:
            board[y][x] = "S"

    if food:
        food_x, food_y = food
        board[food_y][food_x] = "F"


def board_to_string(board):
    """Return board as lines of space-separated cells.

    >>> board_to_string([['H', '.'], ['S', 'F']])
    'H .\\nS F'
    """
    return "\n".join(" ".join(row) for row in board)


def snake_as_pairs(snake_xs, snake_ys):
    """Return [[x, y], ...] representation from coordinate lists.

    >>> snake_as_pairs([2, 1, 0], [0, 0, 0])
    [[2, 0], [1, 0], [0, 0]]
    """
    return [[snake_xs[i], snake_ys[i]] for i in range(len(snake_xs))]


def check_self_collision(snake_xs, snake_ys):
    """Return True if snake head overlaps its body.

    >>> check_self_collision([1, 1, 2], [2, 2, 2])
    True
    >>> check_self_collision([1, 2, 3], [2, 2, 2])
    False
    """
    if not snake_xs:
        return False

    head = (snake_xs[0], snake_ys[0])
    for i in range(1, len(snake_xs)):
        if (snake_xs[i], snake_ys[i]) == head:
            return True
    return False


def move_snake(snake_xs, snake_ys, dx, dy, width, height, food):
    """Move snake by one step with wrap-around.

    Mutates snake_xs/snake_ys and returns True if food was eaten.

    >>> xs, ys = [2, 1, 0], [0, 0, 0]
    >>> move_snake(xs, ys, 1, 0, 5, 5, [4, 4])
    False
    >>> xs, ys
    ([3, 2, 1], [0, 0, 0])

    >>> xs, ys = [0, 1], [0, 0]
    >>> move_snake(xs, ys, -1, 0, 3, 3, [2, 0])
    True
    >>> xs, ys
    ([2, 0, 1], [0, 0, 0])
    """
    new_head_x = (snake_xs[0] + dx) % width
    new_head_y = (snake_ys[0] + dy) % height

    ate_food = [new_head_x, new_head_y] == food

    if ate_food:
        snake_xs.insert(0, new_head_x)
        snake_ys.insert(0, new_head_y)
    else:
        for i in range(len(snake_xs) - 1, 0, -1):
            snake_xs[i] = snake_xs[i - 1]
            snake_ys[i] = snake_ys[i - 1]
        snake_xs[0] = new_head_x
        snake_ys[0] = new_head_y

    return ate_food


def update_direction(curr_dx, curr_dy, key):
    """Return updated [dx, dy] from key, blocking reverse turns.

    >>> update_direction(1, 0, UP)
    [0, -1]
    >>> update_direction(1, 0, LEFT)
    [1, 0]
    >>> update_direction(0, -1, DOWN)
    [0, -1]
    """
    directions = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
    }

    if key not in directions:
        return [curr_dx, curr_dy]

    new_dx, new_dy = directions[key]

    if new_dx == -curr_dx and new_dy == -curr_dy:
        return [curr_dx, curr_dy]

    return [new_dx, new_dy]


def would_collide_after_move(snake_xs, snake_ys, dx, dy, width, height):
    """Return True if next wrapped head position hits current body.

    >>> would_collide_after_move([4, 3], [0, 0], -1, 0, 10, 10)
    True
    >>> would_collide_after_move([4, 3], [0, 0], 1, 0, 10, 10)
    False
    """
    next_x = (snake_xs[0] + dx) % width
    next_y = (snake_ys[0] + dy) % height

    for i in range(1, len(snake_xs)):
        if snake_xs[i] == next_x and snake_ys[i] == next_y:
            return True
    return False

if __name__ == "__main__":
    """The code below reads your doctests and checks correctness.
    Do not change Below code!!"""
    import doctest
    doctest.testmod()

