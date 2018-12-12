import argparse
import collections
import re
from typing import DefaultDict
from typing import NamedTuple
from typing import Pattern

import pytest

from support import timing


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


def compute(s: str) -> int:
    lines = s.splitlines()
    initial_state = lines[0].split()[2]
    transitions = [Transition.parse(s) for s in lines[2:]]

    left = 0
    s = initial_state
    for _ in range(20):
        left -= 5
        s = '.....' + s + '.....'

        res: DefaultDict[int, str] = collections.defaultdict(lambda: '.')

        for i, transition in enumerate(transitions):
            for match in transition.pattern.finditer(s):
                res[match.start() + left] = transition.replacement

        left = min(res)
        s = ''.join(res[i] for i in range(left, max(res) + 1))

    return sum([i + left for i, c in enumerate(s) if c == '#'])


SAMPLE_INPUT = '''\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, 325),
    ),
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
