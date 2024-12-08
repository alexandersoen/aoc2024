from __future__ import annotations

from collections import defaultdict
from functools import partial
from itertools import filterfalse, permutations
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day8.txt"

Problem = tuple[int, list[int]]

AntennaMap = dict[str, list[complex]]
CityDim = tuple[int, int]


def parse_antenna(path: Path) -> tuple[AntennaMap, CityDim]:
    row_count = 0

    antenna_map = defaultdict(list)

    with path.open() as f:
        row = ""
        for i, row in enumerate(f):
            row = row.strip()
            row_count += 1

            for j, v in enumerate(row):
                antenna_map[v].append(complex(i, j))

        col_count = len(row)  #

    # Remove null slot
    del antenna_map["."]

    city_dim = (row_count, col_count)
    return antenna_map, city_dim


def create_antinode_pos_set(antenna_map: AntennaMap) -> set[complex]:
    antinode_pos = set()
    for antenna_pos_list in antenna_map.values():
        for pos1, pos2 in permutations(antenna_pos_list, r=2):
            delta = pos1 - pos2

            antinode1 = pos1 + delta
            antinode2 = pos2 - delta

            antinode_pos.add(antinode1)
            antinode_pos.add(antinode2)

    return antinode_pos


def create_antinode_pos_harmonic_set(
    antenna_map: AntennaMap, city_dim: CityDim
) -> set[complex]:
    antinode_pos = set()
    for antenna_pos_list in antenna_map.values():
        for pos1, pos2 in permutations(antenna_pos_list, r=2):
            delta = pos1 - pos2

            for i in range(city_dim[0] + city_dim[1]):
                antinode_pos.add(pos1 + delta * i)

            for i in range(city_dim[0] + city_dim[1]):
                antinode_pos.add(pos2 - delta * i)

        if len(antenna_pos_list) > 1:
            antinode_pos.update(antenna_pos_list)

    return antinode_pos


def out_of_bounds(pos: complex, city_dim: CityDim) -> bool:
    r, c = pos.real, pos.imag

    if r < 0:
        return True
    if c < 0:
        return True
    if r >= city_dim[0]:
        return True
    if c >= city_dim[1]:
        return True

    return False


def print_city(
    antenna_map: AntennaMap, city_dim: CityDim, antinodes: set[complex]
):
    city = []
    for _ in range(city_dim[0]):
        city.append(["."] * city_dim[1])

    for k, pos_list in antenna_map.items():
        for pos in pos_list:
            r, c = int(pos.real), int(pos.imag)
            city[r][c] = k

    for pos in antinodes:
        r, c = int(pos.real), int(pos.imag)
        city[r][c] = "#"

    print("=" * city_dim[0])
    for row in city:
        for v in row:
            print(v, end="")
        print()
    print("=" * city_dim[0])


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    antenna_map, city_dim = parse_antenna(data_path)

    match part:
        case ProblemParts.Part1:
            antinodes = create_antinode_pos_set(antenna_map)
            antinodes_in_city = set(
                filterfalse(
                    partial(out_of_bounds, city_dim=city_dim), antinodes
                )
            )

            print_city(antenna_map, city_dim, antinodes_in_city)

            count = len(antinodes_in_city)

        case ProblemParts.Part2:
            antinodes = create_antinode_pos_harmonic_set(antenna_map, city_dim)
            antinodes_in_city = set(
                filterfalse(
                    partial(out_of_bounds, city_dim=city_dim), antinodes
                )
            )

            print_city(antenna_map, city_dim, antinodes_in_city)

            count = len(antinodes_in_city)

    print("count:", count)


if __name__ == "__main__":
    main()
