def make_board(width, height):
    board = []
    for row in range(height):
        new_row = []
        for col in range(width):
            new_row.append(' ')
        board.append(new_row)
    return board


def board_to_string(board):
    str_board = ''
    for row in board:
        str_board += ''.join(row) + '\n'
    return str_board


def snake_as_pairs(snake):
    pairs = []
    for index in range(len(snake)):
        pairs.append((snake[index][0], snake[index][1]))
    return pairs


def move_snake(snake, direction):
    head_x = snake[0][0]
    head_y = snake[0][1]

    if direction == 'up':
        new_head = (head_x, head_y - 1)
    elif direction == 'down':
        new_head = (head_x, head_y + 1)
    elif direction == 'left':
        new_head = (head_x - 1, head_y)
    elif direction == 'right':
        new_head = (head_x + 1, head_y)

    snake.insert(0, new_head)
    return snake


def update_direction(current_direction, new_direction):
    if (current_direction == 'up' and new_direction != 'down') or  
       (current_direction == 'down' and new_direction != 'up') or  
       (current_direction == 'left' and new_direction != 'right') or  
       (current_direction == 'right' and new_direction != 'left'):
        return new_direction
    return current_direction


def would_collide_after_move(snake, board, direction):
    head_x = snake[0][0]
    head_y = snake[0][1]
    if direction == 'up':
        head_y -= 1
    elif direction == 'down':
        head_y += 1
    elif direction == 'left':
        head_x -= 1
    elif direction == 'right':
        head_x += 1

    # Check for collision with borders
    if head_x < 0 or head_x >= len(board[0]):
        return True
    if head_y < 0 or head_y >= len(board):
        return True

    # Check for collision with self
    for segment in snake[1:]:
        if segment[0] == head_x and segment[1] == head_y:
            return True

    return False
