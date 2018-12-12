import argparse
import sys
from typing import List

import pytest

from support import timing


def power(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = (power % 1000) // 100
    return power - 5


def compute_orig(s: str) -> str:
    n = int(s)
    maximum = -sys.maxsize
    position = ''

    grid = [[-sys.maxsize] * 301 for _ in range(302)]
    for x in range(1, 301):
        for y in range(1, 301):
            grid[y][x] = power(x, y, n)

    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            total = 0
            for x_offset in range(3):
                for y_offset in range(3):
                    total += grid[y + y_offset][x + x_offset]
            if total > maximum:
                maximum = total
                position = f'{x},{y}'

    return position


def summed_area(x: int, y: int, size: int, table: List[List[int]]) -> int:
    adjust = size
    return (
        0
        + table[y + adjust][x + adjust]
        + table[y][x]
        - table[y][x + adjust]
        - table[y + adjust][x]
    )


def compute(s: str) -> str:
    n = int(s)
    maximum = -sys.maxsize
    position = ''

    grid = [[-sys.maxsize] * 301 for _ in range(302)]
    for x in range(1, 301):
        for y in range(1, 301):
            grid[y][x] = power(x, y, n)

    table = [[0] * 302 for _ in range(302)]
    for y in range(301):
        for x in range(301):
            table[y + 1][x + 1] = (
                0
                + table[y + 1][x] +
                + table[y][x + 1]
                + grid[y][x]
                - table[y][x]
            )

    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            total = summed_area(x, y, 3, table)
            if total > maximum:
                maximum = total
                position = f'{x},{y}'

    return position


@pytest.mark.parametrize(
    ('input_serial', 'expected'),
    (
        ('18', '33,45'),
        ('18\n', '33,45'),
        ('42', '21,61'),
    ),
)
def test(input_serial: str, expected: str) -> None:
    assert compute(input_serial) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing('brute force'):
        print(compute_orig(f.read()))
    with open(args.data_file) as f, timing('summed-area table'):
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
