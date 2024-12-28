import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Counter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import OneClassSVM

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day14.txt"
RE_PATTERN = re.compile(r"=(-?\d+),(-?\d+)")
# WORLD_DIM = 11, 7
WORLD_DIM = 101, 103


@dataclass
class Robot:
    def __init__(self, pos: complex, vel: complex) -> None:
        self.init_pos = pos

        self.pos = pos
        self.vel = vel

    def reset(self) -> None:
        self.pos = self.init_pos

    def step(self) -> None:
        _new_pos = self.pos + self.vel
        new_pos = complex(
            _new_pos.real % WORLD_DIM[0], _new_pos.imag % WORLD_DIM[1]
        )
        self.pos = new_pos


def parse_robots(path: Path) -> list[Robot]:
    robots = list()
    with path.open() as f:
        for row in f:
            pos_str, vel_str = row.strip().split(" ", maxsplit=1)

            pos_match = re.search(RE_PATTERN, pos_str)
            vel_match = re.search(RE_PATTERN, vel_str)

            if pos_match is None or vel_match is None:
                raise ValueError()

            pos = complex(*map(int, pos_match.groups()))
            vel = complex(*map(int, vel_match.groups()))

            robots.append(Robot(pos, vel))

    return robots


def simulate_n_rounds(robots: list[Robot], n: int) -> None:
    for _ in range(n):
        for r in robots:
            r.step()


def score_by_quad(robots: list[Robot]) -> int:
    q1, q2, q3, q4 = 0, 0, 0, 0

    for r in robots:
        if r.pos.real < WORLD_DIM[0] // 2 and r.pos.imag < WORLD_DIM[1] // 2:
            q1 += 1
        elif r.pos.real < WORLD_DIM[0] // 2 and r.pos.imag > WORLD_DIM[1] // 2:
            q2 += 1
        elif r.pos.real > WORLD_DIM[0] // 2 and r.pos.imag < WORLD_DIM[1] // 2:
            q3 += 1
        elif r.pos.real > WORLD_DIM[0] // 2 and r.pos.imag > WORLD_DIM[1] // 2:
            q4 += 1

    return q1 * q2 * q3 * q4


def print_count_array(robots: list[Robot]) -> None:
    counter = Counter()
    for r in robots:
        counter[r.pos] += 1

    for c in range(WORLD_DIM[1]):
        for r in range(WORLD_DIM[0]):
            pos = complex(r, c)
            if counter[pos] > 0:
                print(counter[pos], end="")
            else:
                print(".", end="")

        print()


def to_binary_array(robots: list[Robot]) -> np.ndarray:
    data = np.zeros((WORLD_DIM[1], WORLD_DIM[0]))
    for r in robots:
        data[int(r.pos.imag), int(r.pos.real)] = 1

    return data


def to_prob_array(robots: list[Robot]) -> np.ndarray:
    data = np.zeros((WORLD_DIM[1], WORLD_DIM[0]))
    for r in robots:
        data[int(r.pos.imag), int(r.pos.real)] = 1
    data /= data.sum()

    return data


def to_chunked_prob_array(
    robots: list[Robot], chunk_size: int = 10
) -> np.ndarray:
    data = np.zeros(
        (
            math.ceil(WORLD_DIM[1] / chunk_size),
            math.ceil(WORLD_DIM[0] / chunk_size),
        )
    )
    for r in robots:
        data[int(r.pos.imag) // chunk_size, int(r.pos.real) // chunk_size] += 1
    data /= data.sum()

    return data


def print_nonzero_array(array: np.ndarray) -> None:
    for c in range(WORLD_DIM[1]):
        for r in range(WORLD_DIM[0]):
            if array[c, r] > 0:
                print("#", end="")
            else:
                print(".", end="")

        print()


def calculate_entropy(prob_array: np.ndarray) -> float:
    prob_vec = prob_array.flatten()

    return -(prob_vec * np.log(prob_vec, where=prob_vec > 0)).sum()


def min_entropy(robots: list[Robot], n_steps: int = 10_000) -> int:
    for r in robots:
        r.reset()

    ent_list = list()
    prob_array_list = list()
    for _ in range(n_steps):
        prob_array = to_prob_array(robots)
        chunked_prob_array = to_chunked_prob_array(robots)
        ent = calculate_entropy(chunked_prob_array)

        ent_list.append(ent)
        prob_array_list.append(prob_array)

        for r in robots:
            r.step()

    min_ent_arg = np.argmin(ent_list).item()
    return min_ent_arg


def plot_entropy(robots: list[Robot], n_steps: int = 10_000) -> None:
    for r in robots:
        r.reset()

    ent_list = list()
    for _ in range(n_steps):
        prob_array = to_prob_array(robots)
        ent = calculate_entropy(prob_array)
        ent_list.append(ent)

        for r in robots:
            r.step()

    plt.plot(ent_list)
    plt.show()


def gen_data(robots: list[Robot], n_samples: int = 10_000) -> np.ndarray:
    datas = list()
    for _ in range(n_samples):
        for r in robots:
            r.step()

        datas.append(to_binary_array(robots).reshape(-1))

    for r in robots:
        r.reset()

    return np.vstack(datas)


def lol(robots: list[Robot], n_training_sim: int = 100_000) -> None:
    print("Generating Data")
    data = gen_data(robots, n_samples=n_training_sim)
    model = OneClassSVM()

    print("Fiting One-SVM")
    model.fit(data)

    print("Inference")
    detect = list()
    for _ in range(10_000):
        for r in robots:
            r.step()

        cur_input = gen_data(robots, n_samples=1)
        detect.append(model.score_samples(cur_input))

        print(model.predict(cur_input), model.score_samples(cur_input))

    plt.plot(detect)
    plt.show()


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    robots = parse_robots(data_path)

    match part:
        case ProblemParts.Part1:
            simulate_n_rounds(robots, 100)
            count = score_by_quad(robots)

            print_count_array(robots)

        case ProblemParts.Part2:
            count = min_entropy(robots, 8_000)

    print("count:", count)


if __name__ == "__main__":
    main()
