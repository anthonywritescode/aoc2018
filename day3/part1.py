import argparse
import collections
import re
from typing import DefaultDict

import pytest


PATTERN = re.compile(r'^#(\d)+ @ (\d+),(\d+): (\d+)x(\d+)$')


def compute(s: str) -> int:
    grid:  DefaultDict[int, DefaultDict[int, int]]
    grid = collections.defaultdict(lambda: collections.defaultdict(int))

    for line in s.splitlines():
        match = PATTERN.match(line)
        assert match, line
        left, top = int(match.group(2)), int(match.group(3))
        width, height = int(match.group(4)), int(match.group(5))

        for x in range(left, left + width):
            for y in range(top, top + height):
                grid[x][y] += 1

    total = 0
    for _, row in grid.items():
        for _, val in row.items():
            if val > 1:
                total += 1

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            '#1 @ 1,3: 4x4\n'
            '#2 @ 3,1: 4x4\n'
            '#3 @ 5,5: 2x2\n',

            4,
        ),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
