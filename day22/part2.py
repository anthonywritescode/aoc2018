import argparse
import enum
import functools
import sys
from typing import Dict
from typing import Generator
from typing import Set
from typing import Tuple

import pytest

from support import timing


class Tool(enum.IntEnum):
    TORCH = 1
    CLIMBING_GEAR = 2
    NOTHING = 3


REGION_ROCKY = 0
REGION_WET = 1
REGION_NARROW = 2

REGIONS_TO_TOOLS = {
    REGION_ROCKY: {Tool.TORCH, Tool.CLIMBING_GEAR},
    REGION_WET: {Tool.CLIMBING_GEAR, Tool.NOTHING},
    REGION_NARROW: {Tool.TORCH, Tool.NOTHING},
}


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

    def _region(x: int, y: int) -> int:
        return _erosion_level(x, y) % 3

    start = (0, 0, Tool.TORCH)
    dest = (coord_x, coord_y, Tool.TORCH)
    paths: Set[Tuple[int, int, Tool]] = {start}
    times: Dict[Tuple[int, int, Tool], int] = {start: 0}
    bad_upper_bound = coord_x * 8 + coord_y * 8

    def _legal_and_better(cand: Tuple[int, int, Tool], time: int) -> bool:
        x, y, tool = cand
        return (
            # in bound and valid tool for the region
            x >= 0 and y >= 0 and tool in REGIONS_TO_TOOLS[_region(x, y)] and
            # better time if we've previously gone here
            time < times.get(cand, sys.maxsize) and
            # termination pruning
            time < times.get(dest, bad_upper_bound)
        )

    def _next(
            x: int, y: int, tool: Tool,
    ) -> Generator[Tuple[int, int, Tool], None, None]:
        time = times[(x, y, tool)]
        region_type = _region(x, y)

        # try switching tool first
        cand_time = time + 7
        cand_tool, = REGIONS_TO_TOOLS[region_type] - {tool}
        cand = (x, y, cand_tool)
        if _legal_and_better(cand, cand_time):
            times[cand] = cand_time
            yield cand

        # try moving next
        for x_c, y_c in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            cand_time = time + 1
            cand = (x + x_c, y + y_c, tool)
            if _legal_and_better(cand, cand_time):
                times[cand] = cand_time
                yield cand

    while paths:
        paths = {
            new_path
            for cand_x, cand_y, tool in paths
            for new_path in _next(cand_x, cand_y, tool)
        }

    return times[dest]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            'depth: 510\n'
            'target: 10,10\n',

            45,
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
