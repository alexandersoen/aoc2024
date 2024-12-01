from pathlib import Path
from collections import Counter
from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day1.txt"


def read_to_list_pairs(path: Path) -> tuple[list[int], list[int]]:
    left_list = []
    right_list = []
    with path.open() as f:
        for row in f:
            left, right = row.split("   ")
            left, right = int(left), int(right)

            left_list.append(left)
            right_list.append(right)

    return left_list, right_list


def sorted_distance(list1: list[int], list2: list[int]) -> int:
    list1.sort()
    list2.sort()
    return sum(abs(left - right) for left, right in zip(list1, list2))


def similarity_score(list1: list[int], list2: list[int]) -> int:
    weight = Counter(list2)
    return sum(v * weight[v] for v in list1)


def main():

    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    left_list, right_list = read_to_list_pairs(data_path)

    match part:
        case ProblemParts.Part1:
            dist = sorted_distance(left_list, right_list)
        case ProblemParts.Part2:
            dist = similarity_score(left_list, right_list)

    print(dist)


if __name__ == "__main__":
    main()
