import argparse
from typing import Generator
from typing import List
from typing import Tuple

import pytest

from support import timing


def adjacent(
        y: int, x: int,
        boundy: int, boundx: int,
) -> Generator[Tuple[int, int], None, None]:
    for yadj in range(-1, 2):
        for xadj in range(-1, 2):
            ypt = y + yadj
            xpt = x + xadj
            if (
                    not (ypt == y and xpt == x) and
                    ypt >= 0 and xpt >= 0 and
                    ypt < boundy and xpt < boundx
            ):
                yield (ypt, xpt)


def newchr(c: str, y: int, x: int, grid: List[str]) -> str:
    near = [
        grid[ypt][xpt]
        for ypt, xpt in adjacent(y, x, len(grid), len(grid[0]))
    ]
    if c == '.':
        if near.count('|') >= 3:
            return '|'
        else:
            return '.'
    elif c == '|':
        if near.count('#') >= 3:
            return '#'
        else:
            return '|'
    else:
        if near.count('#') >= 1 and near.count('|') >= 1:
            return '#'
        else:
            return '.'


def compute(s: str) -> int:
    grid = s.splitlines()

    for i in range(10):
        grid = [
            ''.join(newchr(c, y, x, grid) for x, c in enumerate(row))
            for y, row in enumerate(grid)
        ]
    trees = sum(row.count('|') for row in grid)
    lumber = sum(row.count('#') for row in grid)
    return trees * lumber


def test_adjacent() -> None:
    assert len(list(adjacent(1, 2, 50, 50))) == 8
    assert len(list(adjacent(0, 0, 50, 50))) == 3
    assert len(list(adjacent(0, 1, 50, 50))) == 5
    assert len(list(adjacent(0, 1, 2, 2))) == 3


SAMPLE = '''\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE, 1147),
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
