from pathlib import Path
from timeit import timeit

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day2.txt"


def read_reports(path: Path) -> list[list[int]]:
    levels = []
    with path.open() as f:
        for row in f:
            level = row.split(" ")
            level = [int(v) for v in level]
            levels.append(level)

    return levels


def next_idx(idx: int, skip_idx: int | None):
    n_idx = idx + 1
    if n_idx == skip_idx:
        n_idx += 1

    return n_idx


def level_is_safe(
    level: list[int],
    min_jump: int = 1,
    max_jump: int = 3,
    error_allowed: bool = False,
) -> bool:
    diffs = [b - a for a, b in zip(level, level[1:])]
    monotonic = all(v >= 0 for v in diffs) or all(v <= 0 for v in diffs)
    in_bounds = all(min_jump <= abs(v) <= max_jump for v in diffs)

    if monotonic and in_bounds:
        return True
    elif error_allowed:
        for i in range(len(level)):
            new_level = level[:i] + level[i + 1 :]
            if level_is_safe(
                new_level,
                min_jump,
                max_jump,
                error_allowed=False,
            ):
                return True

    return False


def fast_level_is_safe(
    level: list[int],
    min_jump: int = 1,
    max_jump: int = 3,
    skip_idx: int | None = None,
    error_allowed: bool = False,
) -> bool:
    idx1 = next_idx(-1, skip_idx)
    idx2 = next_idx(idx1, skip_idx)
    while idx2 < len(level):
        diff = level[idx2] - level[idx1]

        increasing = diff > 0
        in_bounds = min_jump <= diff <= max_jump
        if increasing and in_bounds:
            idx1, idx2 = next_idx(idx1, skip_idx), next_idx(idx2, skip_idx)
        elif error_allowed:
            return fast_level_is_safe(
                level,
                min_jump,
                max_jump,
                skip_idx=idx2,
                error_allowed=False,
            ) or fast_level_is_safe(
                level,
                min_jump,
                max_jump,
                skip_idx=idx1,
                error_allowed=False,
            )
        else:
            return False

    return True


def fast_monotonic_within_jump_num_sat(
    levels: list[list[int]],
    min_jump: int = 1,
    max_jump: int = 3,
    error_allowed: bool = False,
) -> int:
    count = 0

    for level in levels:
        # Decreasing, make increasing
        if 2 <= sum(b - a < 0 for a, b in zip(level, level[1:])):
            level = [-v for v in level]

        is_safe = fast_level_is_safe(
            level, min_jump, max_jump, error_allowed=error_allowed
        )
        count += int(is_safe)

    return count


def monotonic_within_jump_num_sat(
    levels: list[list[int]],
    min_jump: int = 1,
    max_jump: int = 3,
    error_allowed: bool = False,
) -> int:
    count = 0

    for level in levels:
        is_safe = level_is_safe(
            level, min_jump, max_jump, error_allowed=error_allowed
        )
        count += int(is_safe)

    return count


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    levels = read_reports(data_path)

    match part:
        case ProblemParts.Part1:
            num_sat = monotonic_within_jump_num_sat(
                levels, min_jump=1, max_jump=3, error_allowed=False
            )
        case ProblemParts.Part2:
            print(
                "fast:",
                timeit(
                    lambda: fast_monotonic_within_jump_num_sat(
                        levels, min_jump=1, max_jump=3, error_allowed=True
                    ),
                    number=10,
                ),
            )
            print(
                "brute:",
                timeit(
                    lambda: monotonic_within_jump_num_sat(
                        levels, min_jump=1, max_jump=3, error_allowed=True
                    ),
                    number=10,
                ),
            )
            num_sat = fast_monotonic_within_jump_num_sat(
                levels, min_jump=1, max_jump=3, error_allowed=True
            )

    print(num_sat)


if __name__ == "__main__":
    main()
