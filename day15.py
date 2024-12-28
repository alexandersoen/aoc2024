from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day15.txt"

MoveStr = str
LEFT = 0 - 1j
RIGHT = 0 + 1j
UP = -1 + 0j
DOWN = +1 + 0j


class AbstractMaze(ABC):
    @abstractmethod
    def move(self, dir: complex) -> None:
        pass

    @abstractmethod
    def object_loc_list(self) -> Iterable[complex]:
        pass

    def print(self) -> None:
        pass


class Maze(AbstractMaze):
    def __init__(
        self,
        sub_loc: complex,
        object_set: set[complex],
        wall_set: set[complex],
    ) -> None:
        self.sub_loc = sub_loc
        self.object_set = object_set
        self.wall_set = wall_set

    def object_loc_list(self) -> Iterable[complex]:
        return self.object_set

    def move(self, dir: complex) -> None:
        next_loc = self.sub_loc + dir

        # Check for wall
        if next_loc in self.wall_set:
            return
        # Nothing, then move
        if next_loc not in self.object_set:
            self.sub_loc = next_loc
            return

        # Now need to do the shoving case
        check_loc = next_loc
        while check_loc in self.object_set:
            check_loc += dir

        # Can't shove as wall
        if check_loc in self.wall_set:
            return
        else:
            self.object_set.remove(next_loc)
            self.object_set.add(check_loc)
            self.sub_loc = next_loc

        return


class LargeMaze(AbstractMaze):
    def __init__(
        self,
        sub_loc: complex,
        object_dict: dict[complex, int],
        wall_set: set[complex],
    ) -> None:
        self.sub_loc = sub_loc
        self.object_dict = object_dict
        self.wall_set = wall_set

        id_to_pos = defaultdict(list)
        for pos, id in object_dict.items():
            id_to_pos[id].append(pos)
        self.id_to_pos = {id: tuple(poses) for id, poses in id_to_pos.items()}

    def object_loc_list(self) -> Iterable[complex]:
        return [p[0] for p in self.id_to_pos.values()]

    def move(self, dir: complex) -> None:
        next_loc = self.sub_loc + dir

        # Check for wall
        if next_loc in self.wall_set:
            return
        # Nothing, then move
        if next_loc not in self.object_dict:
            self.sub_loc = next_loc
            return

        # Now need to do the shoving case
        shove_stack = [next_loc]
        move_set = Counter()
        move_list = list()

        # Check if move is valid
        while shove_stack:
            check_loc = shove_stack.pop()

            if check_loc in self.object_dict:
                check_id = self.object_dict[check_loc]
                p1, p2 = self.id_to_pos[check_id]

                # Already seen, can skip checks and stuff
                if move_set[check_id] == 2:
                    continue

                move_set[check_id] += 1
                move_list.append(check_id)
                shove_stack.append(p1 + dir)
                shove_stack.append(p2 + dir)

            # Can't shove as wall
            elif check_loc in self.wall_set:
                return

        # Move everything
        new_obj_pos = dict()
        del_set = set()

        for obj_id in list(set(move_list)):
            p1, p2 = self.id_to_pos[obj_id]

            del_set.add(p1)
            del_set.add(p2)

            new_p1 = p1 + dir
            new_p2 = p2 + dir

            self.id_to_pos[obj_id] = (new_p1, new_p2)

            new_obj_pos[new_p1] = obj_id
            new_obj_pos[new_p2] = obj_id

        for pos in del_set:
            del self.object_dict[pos]

        self.object_dict = self.object_dict | new_obj_pos

        self.sub_loc = next_loc

        return

    def print(self) -> None:
        SIZE = 50
        print()
        for r in range(SIZE):
            for c in range(SIZE * 2):
                pos = complex(r, c)

                if pos == self.sub_loc:
                    print("@", end="")
                elif pos in self.wall_set:
                    print("#", end="")
                elif pos in self.object_dict:
                    print("o", end="")
                else:
                    print(".", end="")

            print()


def parse_sub_map(path: Path) -> tuple[MoveStr, Maze]:
    start_pos = 0
    wall_set = set()
    object_set = set()
    move_str_list = list()

    maze_flag = True

    with path.open() as f:
        for r, row in enumerate(f):
            row = row.strip()

            # Next part of input
            if row == "":
                maze_flag = False
                continue

            if maze_flag:
                for c, v in enumerate(row):
                    pos = complex(r, c)

                    match v:
                        case "#":
                            wall_set.add(pos)
                        case "O":
                            object_set.add(pos)
                        case "@":
                            start_pos = pos
            else:
                move_str_list.append(row)

    maze = Maze(start_pos, object_set, wall_set)
    return "".join(move_str_list), maze


def execute_move_str(maze: AbstractMaze, move_str: str) -> None:
    for m in move_str:
        # print(m)
        match m:
            case "^":
                maze.move(UP)
            case "<":
                maze.move(LEFT)
            case ">":
                maze.move(RIGHT)
            case "v":
                maze.move(DOWN)

        # maze.print()


def pos_score(maze: AbstractMaze) -> int:
    score = 0
    for o in maze.object_loc_list():
        score += o.real * 100 + o.imag

    return int(score)


def to_large_maze(maze: Maze) -> LargeMaze:
    sub_loc = complex(maze.sub_loc.real, 2 * maze.sub_loc.imag)
    object_dict = dict()
    for i, obj_pos in enumerate(maze.object_set):
        object_dict[complex(obj_pos.real, 2 * obj_pos.imag)] = i
        object_dict[complex(obj_pos.real, 2 * obj_pos.imag + 1)] = i

    wall_set = set()
    for i, obj_pos in enumerate(maze.wall_set):
        wall_set.add(complex(obj_pos.real, 2 * obj_pos.imag))
        wall_set.add(complex(obj_pos.real, 2 * obj_pos.imag + 1))

    return LargeMaze(sub_loc, object_dict, wall_set)


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    move_str, maze = parse_sub_map(data_path)

    match part:
        case ProblemParts.Part1:
            execute_move_str(maze, move_str)
            count = pos_score(maze)

        case ProblemParts.Part2:
            maze = to_large_maze(maze)
            execute_move_str(maze, move_str)
            count = pos_score(maze)

    print("count:", count)


if __name__ == "__main__":
    main()
