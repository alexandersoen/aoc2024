from __future__ import annotations

import heapq
from collections import defaultdict
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day16.txt"

State = tuple[complex, int]  # Position, Rotation
DIRS = [1j, 1, -1j, -1]


class Maze:
    def __init__(self, target: complex, wall_set: set[complex]) -> None:
        self.target = target
        self.wall_set = wall_set

    def moves(self, state: State) -> list[tuple[State, float]]:
        pos, r_int = state
        dir = DIRS[r_int]

        next_states = list()
        next_states.append(((pos, (r_int + 1) % 4), 1000.0))
        next_states.append(((pos, (r_int - 1) % 4), 1000.0))
        if pos + dir not in self.wall_set:
            next_states.append(((pos + dir, r_int), 1))

        return next_states

    def score_to_target(self, state: State) -> float:
        return 100 * abs(self.target - state[0])

    def finished(self, state: State) -> bool:
        return (
            state[0].real == self.target.real
            and state[0].imag == self.target.imag
        )


def parse_maze(path: Path) -> tuple[State, Maze]:
    wall_set = set()
    target = -1
    start = -1
    with path.open() as f:
        for r, row in enumerate(f):
            for c, v in enumerate(row):
                pos = complex(r, c)
                if v == "#":
                    wall_set.add(pos)
                elif v == "E":
                    target = pos
                elif v == "S":
                    start = pos

    return (start, 0), Maze(target, wall_set)


class Node:
    def __init__(self, state: State, cost: int, parent=None) -> None:
        self.state = state
        self.cost = cost
        self.parent = parent

    def __lt__(self, other: Node) -> bool:
        return self.cost < other.cost


def search(
    state: State, maze: Maze
) -> tuple[dict[State, State | None], State]:
    check_heap = list()
    visited = set()

    path_dict = dict()

    heapq.heappush(check_heap, Node(state, 0))
    while check_heap:
        cur_node = heapq.heappop(check_heap)
        cur_cost, state = cur_node.cost, cur_node.state

        if state in visited:
            continue

        visited.add(state)
        path_dict[state] = cur_node.parent

        # We are done
        if maze.finished(state):
            break  # return path_dict

        for next_state, next_w in maze.moves(state):
            next_cost = next_w + cur_cost
            heapq.heappush(
                check_heap, Node(next_state, next_cost, parent=state)
            )

    return path_dict, state  # pyright: ignore


def calculate_cost(
    last_state: State, path_dict: dict[State, State | None]
) -> int:
    cur_state = last_state
    cost = 0
    while True:
        print(cur_state)
        prev_state = path_dict[cur_state]

        if prev_state is None:
            break

        if cur_state[0] == prev_state[0]:
            cost += 1000
        else:
            cost += 1

        cur_state = prev_state

    return cost


def calculate_len(
    last_state: State, path_dict: dict[State, State | None]
) -> int:
    cur_state = last_state
    plen = 0
    while True:
        print(cur_state)
        prev_state = path_dict[cur_state]

        if prev_state is None:
            break

        if cur_state[0] != prev_state[0]:
            plen += 1

        cur_state = prev_state

    return plen


class HistNode:
    def __init__(
        self,
        state: State,
        cost: int,
        hist: set[complex],
        hcost: float | None = None,
    ) -> None:
        self.state = state
        self.cost = cost
        self.hist = hist

        hcost = cost

        self.hcost = hcost

    def __lt__(self, other: HistNode) -> bool:
        return self.hcost < other.hcost


def search_all_paths(state: State, maze: Maze) -> int:
    check_heap = list()
    visited_cost = defaultdict(lambda: float("inf"))
    upper_cost = float("inf")
    in_min_path = set()

    heapq.heappush(
        check_heap, HistNode(state, 0, {state[0]}, maze.score_to_target(state))
    )
    while check_heap:
        cur_node = heapq.heappop(check_heap)
        cur_cost, state, hist = cur_node.cost, cur_node.state, cur_node.hist

        if visited_cost[state] < cur_cost:
            continue

        # print(count, cur_cost, upper_cost, visited_cost[state])

        visited_cost[state] = cur_cost

        # Reached finish
        if maze.finished(state):
            upper_cost = cur_cost
            in_min_path |= hist
            continue

        for next_state, next_w in maze.moves(state):
            next_cost = next_w + cur_cost
            next_hcost = next_cost + maze.score_to_target(next_state)
            if next_cost > upper_cost:
                continue

            heapq.heappush(
                check_heap,
                HistNode(
                    next_state, next_cost, hist | {next_state[0]}, next_hcost
                ),
            )

    return len(in_min_path)


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    state, maze = parse_maze(data_path)

    match part:
        case ProblemParts.Part1:
            path_dict, last_state = search(state, maze)
            count = calculate_cost(last_state, path_dict)

        case ProblemParts.Part2:
            count = search_all_paths(state, maze)

    print("count:", count)


if __name__ == "__main__":
    main()
