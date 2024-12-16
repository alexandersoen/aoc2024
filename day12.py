from collections import defaultdict
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day12.txt"

DIRS = [1, 1j, -1, -1j]
R1_DIRS = [1j, -1, -1j, 1]

CROSS_DIRS = [1 + 1j, -1 + 1j, -1 - 1j, -1j + 1]


def get_possible_neighbours(
    pos: complex, valid_set: set[complex]
) -> list[complex]:
    res = []
    for d in DIRS:
        if pos + d in valid_set:
            res.append(pos + d)
    return res


class Garden:
    def __init__(self, plants: dict[str, list[complex]]) -> None:
        self.plants = self.separate_plants(plants)

    def separate_plants(
        self, plants: dict[str, list[complex]]
    ) -> dict[str, list[complex]]:
        new_plants = defaultdict(list)
        for c, pos_list in plants.items():
            pos_set = set(pos_list)
            counter = 0
            while len(pos_set) > 0:
                label = f"{c}_{counter}"
                start_elem = pos_set.pop()
                search_list = [start_elem]

                while len(search_list) > 0:
                    cur_node = search_list.pop()
                    new_plants[label].append(cur_node)

                    next_nodes = get_possible_neighbours(cur_node, pos_set)

                    for n_node in next_nodes:
                        search_list.append(n_node)
                        pos_set.remove(n_node)

                counter += 1

        return new_plants


def parse_garden(path: Path) -> Garden:
    plants = defaultdict(list)
    with path.open() as f:
        for r, row in enumerate(f):
            row = row.strip()
            for c, v in enumerate(row):
                pos = complex(r, c)
                plants[v].append(pos)

    return Garden(plants)


def gen_perimeter_dict(garden: Garden) -> dict[str, int]:
    perimeter_dict = defaultdict(int)
    for c, pos_list in garden.plants.items():
        seen = set()
        for pos in pos_list:
            for d in DIRS:
                npos = pos + d
                if npos in seen:
                    perimeter_dict[c] -= 1
                else:
                    perimeter_dict[c] += 1

                seen.add(pos)

    return perimeter_dict


def corners_at_pos(pos: complex, pos_set: set[complex]) -> int:
    cond_count = sum(d + pos not in pos_set for d in DIRS)
    if cond_count == 4:
        return 4
    elif cond_count == 3:
        return 2

    corners = 0
    for d1, d2 in zip(DIRS, R1_DIRS):
        if pos + d1 in pos_set and pos + d2 in pos_set:
            if (pos + d1 + d2) not in pos_set:
                # inner
                corners += 1
            if ((pos - d1) not in pos_set) and ((pos - d2) not in pos_set):
                # outer
                corners += 1
    return corners


def gen_side_dict(garden: Garden) -> dict[str, int]:
    side_dict = defaultdict(int)
    for c, pos_list in garden.plants.items():
        pos_set = set(pos_list)

        for pos in pos_list:
            side_dict[c] += corners_at_pos(pos, pos_set)

    return side_dict


def calculate_perimeter_cost(garden: Garden):
    cost = 0
    perimeter_dict = gen_perimeter_dict(garden)
    for c, pos_list in garden.plants.items():
        cost += perimeter_dict[c] * len(pos_list)

    return cost


def calculate_side_cost(garden: Garden):
    cost = 0
    side_dict = gen_side_dict(garden)
    for c, pos_list in garden.plants.items():
        cost += side_dict[c] * len(pos_list)

    return cost


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    garden = parse_garden(data_path)

    match part:
        case ProblemParts.Part1:
            count = calculate_perimeter_cost(garden)

        case ProblemParts.Part2:
            count = calculate_side_cost(garden)

    print("count:", count)


if __name__ == "__main__":
    main()
