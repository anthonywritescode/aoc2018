import argparse
import sys

import pytest

from support import timing


def compute(s: str, bound: int) -> int:
    coords = set()
    min_x, min_y = sys.maxsize, sys.maxsize
    max_x, max_y = 0, 0

    for line in s.splitlines():
        xs, ys = line.split(',')
        x, y = int(xs), int(ys)
        max_x, max_y = max(max_x, x), max(max_y, y)
        min_x, min_y = min(min_x, x), min(min_y, y)
        coords.add((x, y))

    total_in_bounds = 0

    adj = bound // len(coords)
    for x in range(min_x - adj, max_x + adj):
        for y in range(min_y - adj, max_y + adj):

            total_distance = 0
            for coord_x, coord_y in coords:
                total_distance += abs(coord_x - x) + abs(coord_y - y)

            if total_distance < bound:
                total_in_bounds += 1

    return total_in_bounds


@pytest.mark.parametrize(
    ('input_s', 'bound', 'expected'),
    (
        (
            '1, 1\n'
            '1, 6\n'
            '8, 3\n'
            '3, 4\n'
            '5, 5\n'
            '8, 9\n',

            32,

            16,
        ),
        ('0, 0\n', 3, 13),
    ),
)
def test(input_s: str, bound: int, expected: int) -> None:
    assert compute(input_s, bound) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    parser.add_argument('--bound', type=int, default=10000)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), args.bound))

    return 0


if __name__ == '__main__':
    exit(main())
