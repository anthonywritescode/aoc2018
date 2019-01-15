import argparse
import collections
from typing import DefaultDict
from typing import List
from typing import NamedTuple

import pytest

from support import every_other
from support import timing


class Point(NamedTuple):
    x: int
    y: int
    z: int
    t: int

    def close_to(self, other: 'Point') -> bool:
        d = sum(abs(d1 - d2) for d1, d2 in zip(self, other))
        return d <= 3

    @classmethod
    def parse(cls, s: str) -> 'Point':
        return cls(*[int(p) for p in s.split(',')])


def compute(s: str) -> int:
    points = [Point.parse(line) for line in s.splitlines()]
    links: DefaultDict[Point, List[Point]] = collections.defaultdict(list)

    for pt1, pt2 in every_other(points):
        if pt1.close_to(pt2):
            links[pt1].append(pt2)
            links[pt2].append(pt1)

    ret = 0
    all_points = set(points)
    while all_points:
        to_traverse = [all_points.pop()]
        while to_traverse:
            pt = to_traverse.pop()
            for link_pt in links[pt]:
                if link_pt in all_points:
                    to_traverse.append(link_pt)
                    all_points.remove(link_pt)
        ret += 1

    return ret


EX1 = '''\
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
'''
EX2 = '''\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
'''
EX3 = '''\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
'''
EX4 = '''\
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (EX1, 2),
        (EX2, 4),
        (EX3, 3),
        (EX4, 8),
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
