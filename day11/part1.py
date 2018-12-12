import argparse
import functools
import sys

import pytest

from support import timing


@functools.lru_cache(maxsize=None)
def power(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = (power % 1000) // 100
    return power - 5


def compute(s: str) -> str:
    n = int(s)
    maximum = -sys.maxsize
    position = ''

    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            total = 0
            for x_offset in range(3):
                for y_offset in range(3):
                    total += power(x + x_offset, y + y_offset, n)
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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
