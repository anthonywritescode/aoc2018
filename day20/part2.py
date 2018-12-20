import argparse
import collections
import sys
from typing import Any
from typing import DefaultDict
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Set
from typing import Tuple
from typing import Union

import pytest

from support import timing


class Or(NamedTuple):
    # mypy recursive types not supported
    choices: Tuple[Tuple[Union[str, Any], ...], ...]


def build_node(s: str, i: int) -> Tuple[Tuple[Union[str, Or], ...], int]:
    ret: List[Union[str, Or]] = ['']

    while i < len(s):
        if s[i] == '|':
            return tuple(ret), i + 1
        elif s[i] == ')':
            return tuple(ret), i
        elif s[i] == '(':
            i += 1
            ornodes: List[Tuple[Union[str, Or], ...]] = []
            while s[i] != ')':
                ornode, i = build_node(s, i)
                ornodes.append(ornode)

            # hax: an empty ornode
            if s[i - 1] == '|':
                ornodes.append(('',))

            ret.extend((Or(tuple(ornodes)), ''))
        else:
            assert isinstance(ret[-1], str), ret[-1]
            ret[-1] += s[i]
        i += 1
    return tuple(ret), i


def traverse(
        px: int, py: int,
        directions: DefaultDict[Tuple[int, int], Set[str]],
        seq: Tuple[Union[str, Or], ...],
) -> Tuple[int, int]:
    for part in seq:
        if isinstance(part, str):
            for c in part:
                if c == 'W':
                    directions[(px, py)].add('W')
                    px -= 1
                    directions[(px, py)].add('E')
                elif c == 'E':
                    directions[(px, py)].add('E')
                    px += 1
                    directions[(px, py)].add('W')
                elif c == 'S':
                    directions[(px, py)].add('S')
                    py += 1
                    directions[(px, py)].add('N')
                elif c == 'N':
                    directions[(px, py)].add('N')
                    py -= 1
                    directions[(px, py)].add('S')
        else:
            px_before, py_before = px, py
            for choice in part.choices:
                px, py = traverse(px_before, py_before, directions, choice)

    return px, py


def next_points(
        px: int,
        py: int,
        directions: Set[str],
) -> Generator[Tuple[int, int], None, None]:
    for direction in directions:
        if direction == 'W':
            yield (px - 1, py)
        elif direction == 'E':
            yield (px + 1, py)
        elif direction == 'S':
            yield (px, py + 1)
        elif direction == 'N':
            yield (px, py - 1)


def compute(s: str) -> int:
    s = s.strip()[1:-1]
    i = 0
    seq, _ = build_node(s, i)

    directions: DefaultDict[Tuple[int, int], Set[str]]
    directions = collections.defaultdict(set)

    traverse(0, 0, directions, seq)

    minx, maxx = sys.maxsize, -sys.maxsize
    miny, maxy = sys.maxsize, -sys.maxsize
    for x, y in directions:
        minx, maxx = min(minx, x), max(maxx, x)
        miny, maxy = min(miny, y), max(maxy, y)

    distance = 0
    seen = {(0, 0): 0}
    pts = [(0, 0)]
    while pts:
        next_pts = []
        for point in pts:
            for cand_point in next_points(*point, directions[point]):
                if cand_point not in seen:
                    seen[cand_point] = distance + 1
                    next_pts.append(cand_point)

        pts = next_pts
        distance += 1

    return sum(d >= 1000 for d in seen.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (),
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
