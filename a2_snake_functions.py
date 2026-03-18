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

def make_board(width: int, height: int) -> list[list[str]]:
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

def clear_board(board: list[list[str]]) -> None:
    """Mutate board so every position becomes ".".

    >>> b = [['H', 'F'], ['S', '.']]
    >>> clear_board(b)
    >>> b
    [['.', '.'], ['.', '.']]
    """
    for y in range(len(board)):
        for x in range(len(board[y])):
            board[y][x] = "."


def place_snake_and_food(board: list[list[str]], 
                         snake: list[list[int]], 
                         food: list[int]) -> None:
    """Clear board, then place snake and food at the specified coordinates.

    Snake is [[x, y], ...] where index 0 is head.

    >>> b = make_board(4, 3)
    >>> place_snake_and_food(b, [[1, 1], [0, 1], [0, 2]], [3, 0])
    >>> b
    [['.', '.', '.', 'F'], ['S', 'H', '.', '.'], ['S', '.', '.', '.']]

    precondition: snake and food must be nonempty.
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


def board_to_string(board: list[list[str]]) -> str:
    """Firstly we turn each column into a comma seperated string, 
    Then we join each row with a newline so that we get a grid representation 
    of the board as a string. 
    """
    return "\n".join(" ".join(row) for row in board)


def snake_as_pairs(snake_xs: list[int], snake_ys: list[int]) -> list[list[int]]:
    """Given a list (snake_xs) of x coordinates for each segment of the snake, and a list
    of y coordinates (snake_ys) pair up each x with a y coordinate according to how they appear 
    in parallel in each list. 

    >>> snake_as_pairs([5, 4, 3], [2, 2, 2])
    [[5, 2], [4, 2], [3, 2]]

    precondition: len(snake_xs) == len(snake_ys)
    Note: I had learned this slick list/string builder notation from stack exchange, I dont recall 
    it being used in class, but it ended up being very useful for this project.
    """

    return [[snake_xs[i], snake_ys[i]] for i in range(len(snake_xs))]


def check_self_collision(snake_xs: list[int], snake_ys: list[int]) -> bool:
    """Return True if snake head overlaps its body. Specifially by identifying the 
    head, and checking the rest of the coordinate pairs to see if they match the head. 
    It parses the snake_xs and snake_ys to locate the parts of the snakeon the board.

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


def move_snake(snake_xs: list[int], snake_ys: list[int], 
               dx: int, dy: int, width: int, 
               height: int, food: list[int]) -> bool:
    """Move the snake forward by one step on a grid with wrap-around.

    The snake's position is represented by two parallel lists:
    `snake_xs` and `snake_ys`, where each index corresponds to a segment
    of the snake's body, and index 0 is the head. The snake moves by adding (dx, dy) to the head position. If the new
    head position goes beyond the grid boundaries, it wraps around using
    modulo arithmetic with the given width and height and if the food was eaten (head index matches food index)
    then the snake grows by one segment.

    Otherwise if food was not eaten, return false and continue as normal.

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


def update_direction(curr_dx: int, curr_dy: int, key: str) -> list[int]:
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


def would_collide_after_move(snake_xs: list[int], 
                             snake_ys: list[int], 
                             dx: int, dy: int, 
                             width: int, height: int) -> bool:
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