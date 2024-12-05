from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Protocol

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day4.txt"


@dataclass
class WordArray:
    array: list[str]
    n_rows: int
    n_cols: int


class WordArrayPosPredicate(Protocol):
    def __call__(self, i: int, j: int, word_array: WordArray) -> int: ...


def read_word_array(path: Path) -> WordArray:
    word_array: list[str] = []
    with path.open() as f:
        for row in f:
            word_array.append(row)

    return WordArray(word_array, len(word_array), len(word_array[0]))


global_check = [[]] * 10
for i in range(len(global_check)):
    global_check[i] = ["."] * 10


def count_xmas_at_pos(i: int, j: int, word_array: WordArray) -> int:
    words_to_check = ["XMAS"]

    count = 0

    for word in words_to_check:
        space_right = j + len(word) <= word_array.n_cols
        space_left = 0 <= j - len(word) + 1
        space_down = i + len(word) <= word_array.n_rows

        # Check right
        if space_right:
            word_check = word_array.array[i][j : j + len(word)]
            # print(word_check, word_check[::-1], word)
            count += int(word_check == word)
            count += int(word_check[::-1] == word)

        # Check down
        if space_down:
            word_check = "".join(
                word_array.array[i + v][j] for v in range(len(word))
            )
            # print(word_check, word)
            count += int(word_check == word)
            count += int(word_check[::-1] == word)

        # Check diagonal right
        if space_down and space_right:
            word_check = "".join(
                word_array.array[i + v][j + v] for v in range(len(word))
            )
            # print(word_check, word)
            count += int(word_check == word)
            count += int(word_check[::-1] == word)

        # Check diagonal left
        if space_down and space_left:
            word_check = "".join(
                word_array.array[i + v][j - v] for v in range(len(word))
            )
            # print(word_check, word)
            count += int(word_check == word)
            count += int(word_check[::-1] == word)

    return count


def count_x_mas_at_pos(i: int, j: int, word_array: WordArray) -> int:
    word = "MAS"

    has_right_space = j + 1 < word_array.n_cols
    has_left_space = 0 <= j
    has_down_space = i + 1 < word_array.n_rows
    has_up_space = 0 <= i

    has_space = (
        has_right_space and has_left_space and has_down_space and has_up_space
    )

    if has_space:
        diag1 = "".join(word_array.array[i + v][j - v] for v in [-1, 0, 1])
        diag2 = "".join(word_array.array[i + v][j + v] for v in [-1, 0, 1])

        diag1_is_mas = (diag1 == word) or (diag1[::-1] == word)
        diag2_is_mas = (diag2 == word) or (diag2[::-1] == word)

        return int(diag1_is_mas and diag2_is_mas)

    return 0


def count_xmas_all(word_array: WordArray, pred: WordArrayPosPredicate) -> int:
    row_iter = range(word_array.n_rows)
    col_iter = range(word_array.n_cols)
    full_iter = product(row_iter, col_iter)
    return sum(pred(i, j, word_array) for i, j in full_iter)


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    word_array = read_word_array(data_path)

    # print("----")
    # print(count_xmas_at_pos(6, 4, word_array))
    # print("----")

    match part:
        case ProblemParts.Part1:
            count = count_xmas_all(word_array, count_xmas_at_pos)
        case ProblemParts.Part2:
            count = count_xmas_all(word_array, count_x_mas_at_pos)

    print("count:", count)


if __name__ == "__main__":
    main()
