from __future__ import annotations

from itertools import product
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day7.txt"

Problem = tuple[int, list[int]]


def parse_problems(path: Path) -> list[Problem]:
    problems = []
    with path.open() as f:
        for row in f:
            target, values = row.strip().split(":", maxsplit=1)
            target = int(target)
            values = [int(v) for v in values.strip().split(" ")]

            problem = (target, values)
            problems.append(problem)

    return problems


def is_calcs_target(
    target: int, problem: list[int], calculations: tuple[int, ...]
) -> bool:
    # Evaluate calculation
    cur_v = problem[0]
    for i, c in enumerate(calculations):
        match c:
            case 0:
                cur_v *= problem[i + 1]
            case 1:
                cur_v += problem[i + 1]
            case _:
                cur_v = int(f"{cur_v}{problem[i+1]}")

        if cur_v > target:
            return False

    return cur_v == target


def check_if_solvable(target: int, values: list[int]) -> bool:
    possible_calcs = product([0, 1], repeat=len(values) - 1)

    for calcs in possible_calcs:
        if is_calcs_target(target, values, calcs):
            return True

    return False


def check_if_solvable_with_concat(target: int, values: list[int]) -> bool:
    possible_calcs = product([0, 1, 2], repeat=len(values) - 1)

    for calcs in possible_calcs:
        if is_calcs_target(target, values, calcs):
            return True

    return False


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    problems = parse_problems(data_path)

    match part:
        case ProblemParts.Part1:
            count = sum(t * int(check_if_solvable(t, vs)) for t, vs in problems)

        case ProblemParts.Part2:
            count = sum(
                t * int(check_if_solvable_with_concat(t, vs))
                for t, vs in problems
            )

    print("count:", count)


if __name__ == "__main__":
    main()
