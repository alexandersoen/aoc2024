from __future__ import annotations

import copy
from enum import Enum
from itertools import product
from pathlib import Path
from typing import Generator

import numpy as np

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day6.txt"


class Direction(Enum):
    North = (-1, 0)
    East = (0, +1)
    South = (+1, 0)
    West = (0, -1)

    def next_dir(self) -> Direction:
        match self:
            case Direction.North:
                next_val = Direction.East
            case Direction.East:
                next_val = Direction.South
            case Direction.South:
                next_val = Direction.West
            case Direction.West:
                next_val = Direction.North

        return next_val


class Maze:
    def __init__(self, maze_list: list[list[int]]) -> None:
        self.maze_array = np.array(maze_list, dtype=np.bool)

    def has_wall(self, pos: tuple[int, int]) -> bool:
        return self.maze_array[*pos]


class Tracker:
    def __init__(self, start_pos: tuple[int, int], maze: Maze) -> None:
        self.start_pos = np.array(start_pos)
        self.maze_shape = maze.maze_array.shape

        self.reset_tracker()

    def reset_tracker(self) -> None:
        self.direction = Direction.North
        self.pos = np.array(self.start_pos)
        self.tracking_array = np.zeros(self.maze_shape, dtype=np.bool)
        self.tracking_array[*self.pos] = 1
        self.loop_check_set = set()

    def next_position(self) -> tuple[int, int] | None:
        next_pos = self.pos + self.direction.value

        if (
            next_pos[0] >= self.tracking_array.shape[0]
            or next_pos[1] >= self.tracking_array.shape[1]
            or next_pos[0] < 0
            or next_pos[1] < 0
        ):
            return None
        return next_pos[0], next_pos[1]

    def forward(self):
        self.pos += self.direction.value
        self.tracking_array[*self.pos] = 1

    def turn(self):
        self.direction = self.direction.next_dir()

    def turn_and_check_loop(self) -> bool:
        self.turn()
        pos_dir = (int(self.pos[0]), int(self.pos[1])) + self.direction.value
        check = pos_dir in self.loop_check_set

        self.loop_check_set.add(pos_dir)

        return check

    def count(self) -> int:
        return self.tracking_array.sum()

    def print(self) -> None:
        for row in self.tracking_array:
            for col in row:
                if col:
                    v = "*"
                else:
                    v = "."

                print(v, end="")

            print()


class MazeChangeGenerator:
    def __init__(
        self, maze: Maze, start_pos: tuple[int, int], path_to_check: np.ndarray
    ) -> None:
        self.maze = maze
        self.start_pos = start_pos
        self.path_to_check = copy.deepcopy(path_to_check)

    def generate_mazes(self) -> Generator[Maze]:
        i_range = range(self.maze.maze_array.shape[0])
        j_range = range(self.maze.maze_array.shape[1])

        for pos in product(i_range, j_range):
            if (
                not self.path_to_check[*pos]
                or self.maze.has_wall(pos)
                or pos == self.start_pos
            ):
                continue

            self.maze.maze_array[*pos] = 1
            yield self.maze
            self.maze.maze_array[*pos] = 0


def read_maze(path: Path) -> tuple[Maze, Tracker]:
    start_pos = (0, 0)
    maze_list = []

    with path.open() as f:
        for i, row in enumerate(f):
            if "^" in row:
                j = row.index("^")
                start_pos = (i, j)

            row_data = [True if s == "#" else False for s in row]
            maze_list.append(row_data)

    maze = Maze(maze_list)
    tracker = Tracker(start_pos, maze)

    return maze, tracker


def track_to_end_and_count(maze: Maze, tracker: Tracker) -> int:
    while True:
        next_pos = tracker.next_position()
        if next_pos is None:
            break

        wall_check = maze.has_wall(next_pos)

        if wall_check:
            tracker.turn()
        else:
            tracker.forward()

    return tracker.count()


def track_for_loops(maze: Maze, tracker: Tracker) -> bool:
    while True:
        next_pos = tracker.next_position()
        if next_pos is None:
            break

        wall_check = maze.has_wall(next_pos)

        if wall_check:
            has_loop = tracker.turn_and_check_loop()
            if has_loop:
                return True

        else:
            tracker.forward()

    return False


def count_potential_loops(maze: Maze, tracker: Tracker) -> int:
    counter = 0
    track_to_end_and_count(maze, tracker)
    maze_gen = MazeChangeGenerator(
        maze, tuple(tracker.start_pos), tracker.tracking_array
    )

    for m in maze_gen.generate_mazes():
        tracker.reset_tracker()
        counter += int(track_for_loops(m, tracker))

    return counter


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    maze, tracker = read_maze(data_path)

    match part:
        case ProblemParts.Part1:
            count = track_to_end_and_count(maze, tracker)
            tracker.print()

        case ProblemParts.Part2:
            count = count_potential_loops(maze, tracker)

    print("count:", count)


if __name__ == "__main__":
    main()
