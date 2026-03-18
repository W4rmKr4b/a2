"""A simple checker for functions in a2_snake_utils.py."""

from typing import Any, Dict
import unittest
import checker_generic
import a2_snake_functions as snake

FILENAME = "a2_snake_functions.py"
PYTA_CONFIG = "a2_pyta.txt"
TARGET_LEN = 79
SEP = "="

CONSTANTS: Dict[str, object] = {}

# Sample data for tests
BOARD_2X2 = [["S", "S"], ["F", "."]]
BOARD_SMALL = [["H", "S", "."], [".", "F", "."]]
SNAKE_PAIRS = [[1, 1], [0, 1], [0, 2]]
FOOD_POS = [3, 0]
SNAKE_XS, SNAKE_YS = [2, 1, 0], [0, 0, 0]
SNAKE_XS_COLLIDE, SNAKE_YS_COLLIDE = [2, 1, 2], [2, 2, 2]


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def test_make_board(self) -> None:
        self._check(snake.make_board, [3, 2], list)

    def test_clear_board(self) -> None:
        b = [row[:] for row in BOARD_2X2]
        self._check(snake.clear_board, [b], type(None))

    def test_place_snake_and_food(self) -> None:
        b = snake.make_board(4, 3)
        s = [[1, 1], [0, 1], [0, 2]]
        f = [3, 0]
        self._check(snake.place_snake_and_food, [b, s, f], type(None))

    def test_board_to_string(self) -> None:
        self._check(snake.board_to_string, [BOARD_SMALL], str)

    def test_snake_as_pairs(self) -> None:
        self._check(snake.snake_as_pairs, [[2, 1, 1], [0, 0, 1]], list)

    def test_check_self_collision(self) -> None:
        self._check(snake.check_self_collision, [SNAKE_XS_COLLIDE, SNAKE_YS_COLLIDE], bool)

    def test_move_snake(self) -> None:
        xs, ys = [2, 1, 0], [0, 0, 0]
        self._check(snake.move_snake, [xs, ys, 1, 0, 5, 5, [4, 4]], bool)

    def test_would_collide_after_move(self) -> None:
        self._check(snake.would_collide_after_move, [[5, 4, 3], [0, 0, 0], -1, 0, 10, 10], bool)

    def test_update_direction(self) -> None:
        self._check(snake.update_direction, [1, 0, "Up"], list)

    def test_check_constants(self) -> None:
        """Values of constants."""
        print("\nChecking that constants refer to their original values")
        self._check_constants(CONSTANTS, snake)
        print("  check complete")

    def _check(self, func: callable, args: list, ret_type: type) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.
        """
        print("\nChecking {}...".format(func.__name__))
        result = checker_generic.check(func, args, ret_type)
        self.assertTrue(result[0], result[1])
        print("  check complete")

    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """
        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = "The value of constant {} should be {} but is {}.".format(
                name, expected, actual
            )
            self.assertEqual(expected, actual, msg)


print("".center(TARGET_LEN, SEP))
print(" Start: checking coding style ".center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(" End checking coding style ".center(TARGET_LEN, SEP))

print(" Start: checking type contracts ".center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(" End checking type contracts ".center(TARGET_LEN, SEP))

print("\nScroll up to see ALL RESULTS:")
print("  - checking coding style")
print("  - checking type contract\n")
