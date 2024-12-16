from dataclasses import dataclass
from pathlib import Path

import numpy as np

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day13.txt"


@dataclass
class Problem:
    matrix: np.ndarray
    target: np.ndarray


def parse_equations(path: Path) -> list[Problem]:
    problems = list()
    counter = 0
    array_list = []
    target_list = []
    with path.open() as f:
        for row in f:
            match counter:
                case 0 | 1:
                    vals = row.split(": ", maxsplit=1)[-1]
                    left, right = vals.split(", ", maxsplit=1)
                    left_v, right_v = (
                        left.split("+", maxsplit=1)[1],
                        right.split("+", maxsplit=1)[1],
                    )
                    array_list.append([int(left_v), int(right_v)])
                case 2:
                    vals = row.split(": ", maxsplit=1)[-1]
                    left, right = vals.split(", ", maxsplit=1)
                    left_v, right_v = (
                        left.split("=", maxsplit=1)[1],
                        right.split("=", maxsplit=1)[1],
                    )
                    target_list.append([[int(left_v)], [int(right_v)]])

                    problems.append(
                        Problem(
                            np.array(array_list, dtype=np.int64).T,
                            np.array(target_list, dtype=np.int64),
                        )
                    )
                    array_list = []
                    target_list = []

            counter = (counter + 1) % 4

    return problems


def count_tokens(problems: list[Problem]) -> int:
    tokens = 0
    for problem in problems:
        res = np.linalg.inv(problem.matrix) @ problem.target
        res = res.squeeze()
        cond = np.abs(np.sum(res - res.round())) < 1e-04

        if cond:
            tokens += res @ np.array([3, 1])
    return int(tokens)


def add_extra(problems: list[Problem]) -> list[Problem]:
    for problem in problems:
        problem.target += 10_000_000_000_000

    return problems


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    problems = parse_equations(data_path)

    match part:
        case ProblemParts.Part1:
            count = count_tokens(problems)

        case ProblemParts.Part2:
            count = count_tokens(add_extra(problems))

    print("count:", count)


if __name__ == "__main__":
    main()
