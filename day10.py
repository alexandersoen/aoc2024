from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day10.txt"

DIRS = [1j, -1j, 1, -1]


@dataclass
class Trail:
    start: list[complex]
    trail_next: dict[complex, list[complex]]
    trail_val: dict[complex, int]

    def next_pos(self, pos: complex) -> list[complex]:
        return self.trail_next[pos]

    def get_val(self, pos: complex) -> int:
        return self.trail_val[pos]


def in_trail_list(pos: complex, trail_list: list[list[int]]) -> bool:
    if int(pos.real) < 0:
        return False
    elif int(pos.real) >= len(trail_list):
        return False
    elif int(pos.imag) < 0:
        return False
    elif int(pos.imag) >= len(trail_list[0]):
        return False

    return True


def parse_trail(path: Path) -> Trail:
    trail_list = list()
    with path.open() as f:
        for row in f:
            trail_row = []
            for v in row.strip():
                if not v.isnumeric():
                    trail_row.append(-2)
                else:
                    trail_row.append(int(v))

            trail_list.append(trail_row)

    trail_next_dict = defaultdict(list)
    trail_val_dict = dict()
    start_list = []
    end_list = []
    for r, row in enumerate(trail_list):
        for c, v in enumerate(row):
            pos = complex(r, c)

            trail_val_dict[pos] = v

            if v == 0:
                start_list.append(pos)

            for d in DIRS:
                n_pos = pos + d
                if (
                    in_trail_list(n_pos, trail_list)
                    and trail_list[int(n_pos.real)][int(n_pos.imag)] == v + 1
                ):
                    trail_next_dict[pos].append(n_pos)

    return Trail(start_list, trail_next_dict, trail_val_dict)


def count_trail_heads(trail: Trail) -> int:
    mem = defaultdict(set)
    count = 0

    def work(pos: complex) -> set[complex]:
        if pos in mem:
            return mem[pos]

        if trail.get_val(pos) == 9:
            mem[pos].add(pos)
            return mem[pos]

        inner_count = set()
        for n_pos in trail.next_pos(pos):
            inner_count = inner_count.union(work(n_pos))

        mem[pos] = inner_count

        return inner_count

    for s_pos in trail.start:
        cur_score = len(work(s_pos))
        count += cur_score

    return count


def count_trail_combinations(trail: Trail) -> int:
    mem = defaultdict(int)
    count = 0

    def work(pos: complex) -> int:
        if pos in mem:
            return mem[pos]

        if trail.get_val(pos) == 9:
            mem[pos] = 1
            return 1

        inner_count = 0
        for n_pos in trail.next_pos(pos):
            inner_count += work(n_pos)

        mem[pos] = inner_count

        return inner_count

    for s_pos in trail.start:
        cur_score = work(s_pos)
        count += cur_score

    return count


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    trail = parse_trail(data_path)

    match part:
        case ProblemParts.Part1:
            count = count_trail_heads(trail)

        case ProblemParts.Part2:
            count = count_trail_combinations(trail)

    print("count:", count)


if __name__ == "__main__":
    main()
