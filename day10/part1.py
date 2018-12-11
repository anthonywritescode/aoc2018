import argparse
import collections
import re
from typing import DefaultDict
from typing import List
from typing import NamedTuple
from typing import Tuple

import pytest

from support import timing

PATTERN = re.compile(r'(-?\d+)')


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':  # type: ignore
        return self._replace(x=self.x + other.x, y=self.y + other.y)


class Vector(NamedTuple):
    position: Point
    velocity: Point

    @classmethod
    def parse(cls, s: str) -> 'Vector':
        x, y, vx, vy = PATTERN.findall(s)
        return cls(Point(int(x), int(y)), Point(int(vx), int(vy)))

    def update(self) -> 'Vector':
        return self._replace(position=self.position + self.velocity)


def min_max(vectors: List[Vector]) -> Tuple[int, int, int, int]:
    min_x = min(vector.position.x for vector in vectors)
    min_y = min(vector.position.y for vector in vectors)
    max_x = max(vector.position.x for vector in vectors)
    max_y = max(vector.position.y for vector in vectors)
    return min_x, max_x, min_y, max_y


def plot(vectors: List[Vector]) -> str:
    grid: DefaultDict[int, DefaultDict[int, str]]
    grid = collections.defaultdict(
        lambda: collections.defaultdict(lambda: '.')
    )
    min_x, max_x, min_y, max_y = min_max(vectors)

    for v in vectors:
        grid[v.position.y][v.position.x] = '#'

    return '\n'.join(
        ''.join(grid[y][x] for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def area(vectors: List[Vector]) -> int:
    min_x, max_x, min_y, max_y = min_max(vectors)
    return (max_x - min_x) * (max_y - min_y)


def compute(s: str) -> str:
    prev_vectors = [Vector.parse(line) for line in s.splitlines()]
    prev_area = area(prev_vectors)

    while True:
        new_vectors = [vector.update() for vector in prev_vectors]
        new_area = area(new_vectors)

        if new_area > prev_area:
            return plot(prev_vectors)
        else:
            prev_vectors = new_vectors
            prev_area = new_area


def test_point_add() -> None:
    assert Point(1, 2) + Point(-3, 4) == Point(-2, 6)


SAMPLE_INPUT = '''\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
'''

SAMPLE_OUTPUT = '''\
#...#..###
#...#...#.
#...#...#.
#####...#.
#...#...#.
#...#...#.
#...#...#.
#...#..###
'''.rstrip()


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, SAMPLE_OUTPUT),
    ),
)
def test(input_s: str, expected: str) -> None:
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
