import argparse
import re
import sys
from typing import List
from typing import Match
from typing import NamedTuple
from typing import Set

import pytest

from support import timing

PATTERN = re.compile(r'^([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)$')
WALLED_IN = re.compile(r'(?<=#)\.*\|[.|]*(?=#)')


class Point(NamedTuple):
    x: int
    y: int


def print_grid(grid: List[List[str]]) -> None:
    print('=' * 79)
    print('\n'.join(''.join(row) for row in grid))
    print('=' * 79)


def compute(s: str) -> int:
    points: List[Point] = []
    min_y, max_y = sys.maxsize, -sys.maxsize
    min_x, max_x = sys.maxsize, -sys.maxsize

    for line in s.splitlines():
        match = PATTERN.match(line)
        assert match, line
        for val in range(int(match[4]), int(match[5]) + 1):
            point = Point(**{match[1]: int(match[2]), match[3]: val})
            points.append(point)
            min_y, max_y = min(point.y, min_y), max(point.y, max_y)
            min_x, max_x = min(point.x - 1, min_x), max(point.x + 1, max_x)

    grid = [
        ['.' for _ in range(min_x, max_x + 1)]
        for _ in range(0, max_y + 1)
    ]
    for point in points:
        grid[point.y][point.x - min_x] = '#'
    grid[0][500 - min_x] = '+'

    down_bound = 0
    up_bound = 0

    modifications = True
    while modifications:
        modifications = False

        # scan down to propogate `|`s
        prev_up_bound = up_bound
        prev_row_pipes: Set[int] = set()
        for rownum, row in enumerate(grid[down_bound:], down_bound):
            row_modifications = False
            next_row_pipes: Set[int] = set()

            for i, c in enumerate(row):
                if c == '.' and i in prev_row_pipes:
                    row_modifications = True
                    row[i] = '|'
                    next_row_pipes.add(i)
                elif c in '+|':
                    next_row_pipes.add(i)

            prev_row_pipes = next_row_pipes
            modifications |= row_modifications

            if row_modifications:
                up_bound = rownum + 1

            if (
                    not row_modifications and
                    rownum != down_bound and
                    rownum >= prev_up_bound
            ):
                break
        else:
            up_bound = len(grid)

        prev_down_bound = down_bound
        prev_row_floor: Set[int] = set()
        for rownum, row in reversed(tuple(enumerate(grid[:up_bound + 1]))):
            row_modifications = False
            next_row_floor: Set[int] = set()

            for i, c in enumerate(row):
                if c in '~#':
                    next_row_floor.add(i)

            def replace_cb(match: Match[str]) -> str:
                needs_floor = set(range(match.start(), match.end() + 1))
                if needs_floor < prev_row_floor:
                    next_row_floor.update(needs_floor)
                    return '~' * len(match.group())
                else:
                    return match.group()

            line = ''.join(row)
            line_after = WALLED_IN.sub(replace_cb, line)
            if line_after != line:
                row_modifications = True
                row[:] = line_after

            for i, c in enumerate(row):
                if c == '|':
                    j = i - 1
                    while (
                            j >= 0 and
                            row[j] == '.'
                            and j + 1 in prev_row_floor
                    ):
                        row_modifications = True
                        row[j] = '|'
                        j -= 1

                    k = i + 1
                    while (
                            k < len(row) and
                            row[k] == '.' and
                            k - 1 in prev_row_floor
                    ):
                        row_modifications = True
                        row[k] = '|'
                        k += 1

            prev_row_floor = next_row_floor
            modifications |= row_modifications

            if row_modifications:
                down_bound = rownum

            if (
                    not row_modifications and
                    rownum != up_bound and
                    rownum <= prev_down_bound
            ):
                break

    return sum(row.count('|') + row.count('~') for row in grid[min_y:])


SAMPLE = '''\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
'''

TEST1 = '''\
x=490, y=5..10
x=510, y=5..10
y=10, x=490..510
x=480, y=15..25
x=500, y=15..25
y=25, x=480..500
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE, 57),
        (TEST1, 360),
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
