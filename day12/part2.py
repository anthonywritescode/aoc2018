import argparse
import collections
import re
from typing import DefaultDict
from typing import Dict
from typing import NamedTuple
from typing import Pattern
from typing import Tuple

import pytest

from support import timing

LEADING_DOTS = re.compile(r'^\.*')


class Transition(NamedTuple):
    pattern: Pattern[str]
    replacement: str

    @classmethod
    def parse(cls, s: str) -> 'Transition':
        pattern, _, replacement = s.split()
        pattern = '(?<={}){}(?={})'.format(
            re.escape(pattern[:2]),
            re.escape(pattern[2]),
            re.escape(pattern[3:])
        )
        return cls(re.compile(pattern), replacement)


FIVE_B = 50000000000


def compute(s: str) -> int:
    lines = s.splitlines()
    initial_state = lines[0].split()[2]
    transitions = [Transition.parse(s) for s in lines[2:]]

    gen = 0
    left = 0
    s = initial_state
    # str -> gen, left
    seen: Dict[str, Tuple[int, int]] = {s: (0, left)}

    while gen < FIVE_B:
        gen += 1
        left -= 5
        s = '.....' + s + '.....'

        res: DefaultDict[int, str] = collections.defaultdict(lambda: '.')

        for i, transition in enumerate(transitions):
            for match in transition.pattern.finditer(s):
                res[match.start() + left] = transition.replacement

        left = min(res)
        s = ''.join(res[i] for i in range(left, max(res) + 1))
        leading_dots_match = LEADING_DOTS.match(s)
        assert leading_dots_match
        left += len(leading_dots_match.group())
        s = s.strip('.')

        # we eventually hit a loop, jump ahead when that occurs
        if s in seen:
            seen_gen, seen_left = seen[s]
            step = gen - seen_gen
            steps = (FIVE_B - gen) // step
            gen += steps * step
            left += steps * (left - seen_left)
        else:
            seen[s] = (gen, left)

    return sum([i + left for i, c in enumerate(s) if c == '#'])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (),  # no samples this time!
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
