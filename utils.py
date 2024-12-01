from argparse import ArgumentParser
from enum import Enum, auto
from typing import cast


class ProblemParts(Enum):
    Part1 = "Part 1"
    Part2 = "Part 2"


def simple_parser_to_part() -> ProblemParts:

    parser = ArgumentParser()
    parser.add_argument("--first-part", action="store_true")

    args = parser.parse_args()
    part = ProblemParts.Part1 if args.first_part else ProblemParts.Part2

    print(f"Calculating result for {part.value}:")

    return part
