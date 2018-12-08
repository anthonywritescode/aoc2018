import argparse
import collections
from typing import Counter
from typing import Optional
from typing import Set
from typing import Tuple

import pytest


def min_coord_by_position(
        x: int,
        y: int,
        coords: Set[Tuple[int, int]],
        max_x: int,
        max_y: int,
) -> Optional[Tuple[int, int]]:
    min_distance = (max_x + 1) * (max_y + 1)
    min_coord: Optional[Tuple[int, int]] = None

    for coord_x, coord_y in coords:
        distance = abs(coord_x - x) + abs(coord_y - y)
        if distance == min_distance:
            min_coord = None
        elif distance < min_distance:
            min_distance = distance
            min_coord = (coord_x, coord_y)

    return min_coord


def compute(s: str) -> int:
    coords = set()
    max_x, max_y = 0, 0

    for line in s.splitlines():
        xs, ys = line.split(',')
        x, y = int(xs), int(ys)
        max_x, max_y = max(max_x, x), max(max_y, y)
        coords.add((x, y))

    counts_by_coord: Counter[Tuple[int, int]] = collections.Counter()

    for x in range(max_x):
        for y in range(max_y):
            min_coord = min_coord_by_position(x, y, coords, max_x, max_y)
            if min_coord is not None:
                counts_by_coord[min_coord] += 1

    for x in range(max_x):
        for y in (-1, max_y + 1):
            min_coord = min_coord_by_position(x, y, coords, max_x, max_y)
            if min_coord is not None:
                counts_by_coord.pop(min_coord, None)

    for y in range(max_y):
        for x in (-1, max_x + 1):
            min_coord = min_coord_by_position(x, y, coords, max_x, max_y)
            if min_coord is not None:
                counts_by_coord.pop(min_coord, None)

    (_, area), = counts_by_coord.most_common(1)
    return area


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            '1, 1\n'
            '1, 6\n'
            '8, 3\n'
            '3, 4\n'
            '5, 5\n'
            '8, 9\n',

            17,
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
