from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day11.txt"


def parse_to_stone_dict(path: Path) -> dict[int, int]:
    res = dict()
    with path.open() as f:
        vals = f.readline().strip().split(" ")
        for v in vals:
            res[int(v)] = 1

    return res


@lru_cache
def stone_update(stone: int) -> list[int]:
    stone_str = str(stone)
    if stone == 0:
        return [1]
    elif len(stone_str) % 2 == 0:
        left, right = (
            stone_str[len(stone_str) // 2 :],
            stone_str[: len(stone_str) // 2],
        )
        return [int(left), int(right)]
    else:
        return [stone * 2024]


def n_update_stone_dict(stone_dict: dict[int, int], n: int) -> dict[int, int]:
    for _ in range(n):
        next_stone_dict = defaultdict(int)
        for k, v in stone_dict.items():
            new_stones = stone_update(k)

            for s in new_stones:
                next_stone_dict[s] += v

        stone_dict = next_stone_dict

    return stone_dict


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    stone_dict = parse_to_stone_dict(data_path)

    match part:
        case ProblemParts.Part1:
            count = sum(v for v in n_update_stone_dict(stone_dict, 25).values())

        case ProblemParts.Part2:
            count = sum(v for v in n_update_stone_dict(stone_dict, 75).values())

    print("count:", count)


if __name__ == "__main__":
    main()
