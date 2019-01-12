import argparse
import re
from typing import List
from typing import NamedTuple

import pytest

from support import timing

INT = re.compile(r'-?\d+')


class Bot(NamedTuple):
    x: int
    y: int
    z: int
    r: int

    def in_range(self, bot: 'Bot') -> bool:
        d = abs(bot.x - self.x) + abs(bot.y - self.y) + abs(bot.z - self.z)
        return d <= self.r


def compute(s: str) -> int:
    bots: List[Bot] = []

    for line in s.splitlines():
        ints = [int(p) for p in INT.findall(line)]
        bots.append(Bot(*ints))

    strong_bot = bots[0]
    for bot in bots:
        if bot.r > strong_bot.r:
            strong_bot = bot

    return sum(strong_bot.in_range(bot) for bot in bots)


SAMPLE_INPUT = '''\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, 7),
        (SAMPLE_INPUT + '<pos=-5,-1,0>, r=6>', 2),
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
