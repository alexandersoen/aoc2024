import copy
from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path

from utils import ProblemParts, simple_parser_to_part

DATA_PATH_STR = "data/day3.txt"


# def read_code(path: Path) -> list[str]:
def read_code(path: Path) -> str:
    strs: list[str] = []
    with path.open() as f:
        for row in f:
            strs.append(row)

    return "".join(strs)


class ParseRes(Enum):
    Fail = auto()
    PartialSuccess = auto()
    FullSuccess = auto()


class State(ABC):
    @abstractmethod
    def predicate(self, t: str) -> bool:
        pass

    def eval(self, tokens: str) -> tuple[ParseRes, State, int | None, str]:
        t = tokens[0]
        parse_res = ParseRes.FullSuccess if self.predicate(t) else ParseRes.Fail
        return parse_res, self, None, tokens[1:]


class CharMatch(State):
    def __init__(self, char: str) -> None:
        self.char = char

    def predicate(self, t: str) -> bool:
        return t == self.char


class DigitParse(State):
    def __init__(self, early_end: str, max_count: int = 3) -> None:
        assert max_count >= 1

        self.count = max_count
        self.early_end = early_end
        self.value_str = ""

    def predicate(self, t: str) -> bool:
        return t.isdigit()

    def eval(self, tokens: str) -> tuple[ParseRes, State, int | None, str]:
        t = tokens[0]
        next_tokens = tokens[1:]

        value = None
        if self.predicate(t):
            self.count -= 1
            self.value_str += t

            if self.count <= 0:
                parse_res = ParseRes.FullSuccess
                value = int(self.value_str)
            else:
                parse_res = ParseRes.PartialSuccess
        else:
            if t == self.early_end:
                parse_res = ParseRes.FullSuccess
                value = int(self.value_str)
                next_tokens = tokens
            else:
                parse_res = ParseRes.Fail

        return parse_res, self, value, next_tokens


class StateMachine:
    def __init__(self, states: list[State]) -> None:
        self.states = states
        self.cur_state = copy.deepcopy(states[0])
        self.state_idx = 0
        self.values: list[int] = []

        self.count = 0

    def parse(self, tokens: str) -> str:
        res, updated_state, value, next_tokens = self.cur_state.eval(tokens)

        match res:
            case ParseRes.Fail:
                self.cur_state = copy.deepcopy(self.states[0])
                self.values = []
                self.state_idx = 0
            case ParseRes.PartialSuccess:
                self.cur_state = updated_state
            case ParseRes.FullSuccess:
                self.state_idx += 1

                if self.state_idx < len(self.states):
                    self.cur_state = copy.deepcopy(self.states[self.state_idx])
                    if value is not None:
                        self.values.append(value)
                else:
                    self.count += self.values[0] * self.values[1]
                    print(self.values, self.count)

                    # Reset
                    self.cur_state = copy.deepcopy(self.states[0])
                    self.values = []
                    self.state_idx = 0
        return next_tokens


def run_state_machine(tokens: str, states: list[State]) -> int:
    sm = StateMachine(states)

    while tokens:
        tokens = sm.parse(tokens)

    return sm.count


def do_dont_filter(tokens: str) -> str:
    """
    Could have made this a state machine as well...
    """
    do_str = "do()"
    dont_str = "don't()"

    parsing_dont = True

    filtered_list = []
    cur_str = copy.deepcopy(tokens)
    while True:
        if parsing_dont:
            res = cur_str.split(dont_str, 1)
            # xxxx dont xxx
            if len(res) > 1:
                filtered_list.append(res[0])
                cur_str = res[1]
                parsing_dont = False
            else:
                filtered_list.append(cur_str)
                break
        else:
            res = cur_str.split(do_str, 1)
            # xxxxxxx do xxxxx
            if len(res) > 1:
                cur_str = res[1]
                parsing_dont = True
            else:
                break

    return "|".join(filtered_list)


def main() -> None:
    part = simple_parser_to_part()

    data_path = Path(DATA_PATH_STR)
    code = read_code(data_path)

    if part == ProblemParts.Part2:
        code = do_dont_filter(code)

    states = [
        CharMatch("m"),
        CharMatch("u"),
        CharMatch("l"),
        CharMatch("("),
        DigitParse(",", max_count=3),
        CharMatch(","),
        DigitParse(")", max_count=3),
        CharMatch(")"),
    ]

    count = run_state_machine(code, states)
    print(count)


if __name__ == "__main__":
    main()
