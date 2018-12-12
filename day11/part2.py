import argparse
import sys

import pytest

from support import timing


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
    res = ''

    grid = [[-sys.maxsize] * 301 for _ in range(302)]
    for x in range(1, 301):
        for y in range(1, 301):
            grid[y][x] = power(x, y, n)

    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            total = grid[y][x]
            if total > maximum:
                maximum = total
                res = f'{x},{y},1'
            for size in range(1, min(300 - x, 300 - y)):
                total += grid[y + size][x + size]
                for i in range(size):
                    total += grid[y + size][x + i]
                    total += grid[y + i][x + size]
                if total > maximum:
                    maximum = total
                    res = f'{x},{y},{size + 1}'

    return res


@pytest.mark.parametrize(
    ('input_serial', 'expected'),
    (
        ('18', '90,269,16'),
        ('18\n', '90,269,16'),
        ('42', '232,251,12'),
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


def visualize_positive() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('serial', type=int)
    args = parser.parse_args()

    for y in range(1, 301):
        for x in range(1, 301):
            if power(x, y, args.serial) > 0:
                print('*', end='')
            else:
                print(' ', end='')
        print()
    return 0


if __name__ == '__main__':
    exit(main())
