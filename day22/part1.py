import argparse
import functools

import pytest

from support import timing


def compute(s: str) -> int:
    _, depth_s, _, coord_s = s.split()
    coord_x_s, coord_y_s = coord_s.split(',')
    depth, coord_x, coord_y = int(depth_s), int(coord_x_s), int(coord_y_s)

    @functools.lru_cache(maxsize=None)
    def _erosion_level(x: int, y: int) -> int:
        return (_geologic_index(x, y) + depth) % 20183

    @functools.lru_cache(maxsize=None)
    def _geologic_index(x: int, y: int) -> int:
        if y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        elif (x, y) == (coord_x, coord_y):
            return 0
        else:
            return _erosion_level(x - 1, y) * _erosion_level(x, y - 1)

    total = 0
    for x in range(coord_x + 1):
        for y in range(coord_y + 1):
            total += _erosion_level(x, y) % 3

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            'depth: 510\n'
            'target: 10,10\n',

            114,
        ),
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
