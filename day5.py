from functools import cmp_to_key
from pathlib import Path
from typing import DefaultDict

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day5.txt"


class BreakRules:
    def __init__(self, rule_tuples: list[tuple[int, int]]) -> None:
        self.break_rule_dict = DefaultDict(set)
        for left, right in rule_tuples:
            self.break_rule_dict[right].add(left)

    def __call__(self, x: int) -> set[int]:
        return self.break_rule_dict[x]

    def is_in(self, x: int) -> bool:
        return x in self.break_rule_dict


def read_problem(path: Path) -> tuple[BreakRules, list[list[int]]]:
    rules = []
    pages = []

    parsing_rules = True
    with path.open() as f:
        for row in f:
            row = row.strip()

            if row == "":
                parsing_rules = False
                continue

            if parsing_rules:
                left, right = row.split("|", 1)
                rules.append((int(left), int(right)))
            else:
                page = [int(v) for v in row.split(",")]
                pages.append(page)

    return BreakRules(rules), pages


def check_rules(rules: BreakRules, page: list[int]) -> bool:
    for i in range(len(page) - 1):
        cur_checks = rules(page[i])
        for j in range(i + 1, len(page)):
            if page[j] in cur_checks:
                return False

    return True


def sum_true_mids(rules: BreakRules, pages: list[list[int]]) -> int:
    count = 0

    for page in pages:
        if check_rules(rules, page):
            count += page[len(page) // 2]

    return count


def fix_page(rules: BreakRules, page: list[int]) -> list[int]:
    def cmp(a, b):
        # Good
        if b in rules(a):
            return -1
        # Bad
        elif a in rules(b):
            return +1
        # Neutral
        else:
            return 0

    return sorted(page, key=cmp_to_key(cmp))


def fix_and_sum_mids(rules: BreakRules, pages: list[list[int]]) -> int:
    count = 0

    for page in pages:
        if not check_rules(rules, page):
            fixed_page = fix_page(rules, page)
            count += fixed_page[len(page) // 2]

    return count


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    rules, pages = read_problem(data_path)

    match part:
        case ProblemParts.Part1:
            count = sum_true_mids(rules, pages)
        case ProblemParts.Part2:
            count = fix_and_sum_mids(rules, pages)

    print("count:", count)


if __name__ == "__main__":
    main()
