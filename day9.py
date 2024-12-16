from itertools import filterfalse
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day9.txt"


def parse_block_code(path: Path) -> str:
    with path.open() as f:
        return f.readline().strip()


def is_space(idx: int) -> bool:
    return bool(idx % 2)


def char_compress_checksum(code: str) -> int:
    # checksum = 0
    checksum_idx = 0
    checksum_left_id = 0
    checksum_right_id = len(code) // 2

    checksum_str = []

    left_idx, right_idx = 0, len(code) - 1
    if is_space(right_idx):
        right_idx -= 1

    left_count, right_count = int(code[left_idx]), int(code[right_idx])
    while not (left_idx >= right_idx and is_space(left_idx)):
        if right_count == 0:
            # Move pointer on right
            right_idx -= 2  # Get to next non-space
            right_count = int(code[right_idx])
            checksum_right_id -= 1
        elif is_space(left_idx) and left_count != 0:
            # Move right to left
            left_count -= 1
            right_count -= 1

            # checksum += checksum_idx * checksum_right_id
            checksum_idx += 1
            checksum_str.append(checksum_right_id)
        elif is_space(left_idx) and left_count == 0:
            left_idx += 1
            left_count = int(code[left_idx])
        elif left_count != 0:
            left_count -= 1
            # checksum += checksum_idx * checksum_left_id
            checksum_idx += 1
            checksum_str.append(checksum_left_id)
        else:
            checksum_left_id += 1
            left_idx += 1

            # set up a count as the new empty block size given
            left_count = int(code[left_idx])

    n_char = sum(int(v) for i, v in enumerate(code) if not is_space(i))
    return sum(i * v for i, v in enumerate(checksum_str[:n_char]))


def block_compress_checksum(code: str) -> int:
    checksum_idx = 0
    checksum_left_id = 0

    checksum_str = []

    rev_block_id_size_list = list(
        reversed(
            list(
                enumerate(
                    list(
                        int(size)
                        for (id, size) in enumerate(code)
                        if not is_space(id)
                    )
                )
            )
        )
    )
    print(rev_block_id_size_list)
    id_seen_flags = [False for _ in range(len(rev_block_id_size_list))]

    (left_idx) = 0

    left_count = int(code[left_idx])
    while left_idx < len(code):
        if is_space(left_idx) and left_count == 0:
            left_idx += 1
            left_count = int(code[left_idx])
        elif is_space(left_idx):
            # Space to push
            space_to_push = left_count

            # left is not space, now scan from right
            push_flag = False
            size = 0
            for id, size in filterfalse(
                lambda i_v: id_seen_flags[i_v[0]], rev_block_id_size_list
            ):
                if size <= space_to_push:
                    print("pushing", space_to_push, (id, size))
                    for _ in range(size):
                        checksum_str.append(id)

                    id_seen_flags[id] = True
                    push_flag = True
                    left_count -= size
                    break

            if not push_flag:
                for _ in range(space_to_push):
                    checksum_str.append(".")

                left_count = 0

        elif left_count != 0:
            left_count -= 1
            # checksum += checksum_idx * checksum_left_id
            checksum_idx += 1

            v = checksum_left_id
            if id_seen_flags[checksum_left_id]:
                v = "."

            checksum_str.append(v)
        else:
            id_seen_flags[checksum_left_id] = True

            checksum_left_id += 1
            left_idx += 1

            # set up a count as the new empty block size given
            next_left_idx = min(left_idx, len(code) - 1)
            left_count = int(code[next_left_idx])

    print(checksum_str)

    return sum(i * v for i, v in enumerate(checksum_str) if v != ".")


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    block_code = parse_block_code(data_path)

    match part:
        case ProblemParts.Part1:
            count = char_compress_checksum(block_code)

        case ProblemParts.Part2:
            count = block_compress_checksum(block_code)

    print("count:", count)


if __name__ == "__main__":
    main()
