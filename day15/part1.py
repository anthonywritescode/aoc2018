import argparse
import bisect
from typing import Dict
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Set
from typing import Tuple

import pytest

from support import timing


class Unit(NamedTuple):
    y: int
    x: int
    unit_type: str


def print_field(
        field: List[List[str]],
        hps: Dict[Tuple[int, int], int],
        units: List[Unit],
) -> None:
    for y, row in enumerate(field):
        print(''.join(row), end='    ')
        print(
            ', '.join(
                f'{unit.unit_type}({hps[(unit.y, unit.x)]})'
                for unit in units
                if unit.y == y
            )
        )


def adjacent(y: int, x: int) -> Generator[Tuple[int, int], None, None]:
    # in reading order
    yield (y - 1, x)
    yield (y, x - 1)
    yield (y, x + 1)
    yield (y + 1, x)


def compute(s: str) -> int:
    field = [list(line) for line in s.splitlines()]
    units: List[Unit] = []
    hps: Dict[Tuple[int, int], int] = {}
    for y, row in enumerate(field):
        for x, c in enumerate(row):
            if c in 'EG':
                unit = Unit(y, x, c)
                units.append(unit)
                hps[(unit.y, unit.x)] = 200

    i = 0
    while True:
        for unit in tuple(units):
            if unit not in units:  # unit was killed earlier
                continue

            targets = [x for x in units if x.unit_type != unit.unit_type]
            if not targets:
                return i * sum(hps.values())

            in_range: Set[Tuple[int, int]] = set()
            for target in targets:
                for y, x in adjacent(target.y, target.x):
                    if field[y][x] == '.' or (y, x) == (unit.y, unit.x):
                        in_range.add((y, x))

            # path to a target
            if (unit.y, unit.x) not in in_range:
                seen = {(unit.y, unit.x): (-1, -1)}
                last = [(unit.y, unit.x)]
                while last:
                    new_last = []
                    for last_y, last_x in last:
                        for cand_y, cand_x in adjacent(last_y, last_x):
                            if (
                                    (cand_y, cand_x) not in seen and
                                    field[cand_y][cand_x] == '.'
                            ):
                                new_last.append((cand_y, cand_x))
                                seen[(cand_y, cand_x)] = (last_y, last_x)

                    if seen.keys() & in_range:
                        break

                    last = new_last
                else:  # never pathed to an in_range square
                    continue

                chosen_y, chosen_x = min(seen.keys() & in_range)
                while seen[(chosen_y, chosen_x)] != (unit.y, unit.x):
                    chosen_y, chosen_x = seen[(chosen_y, chosen_x)]

                hp = hps.pop((unit.y, unit.x))
                field[unit.y][unit.x] = '.'
                units.remove(unit)

                unit = unit._replace(y=chosen_y, x=chosen_x)

                hps[(unit.y, unit.x)] = hp
                field[unit.y][unit.x] = unit.unit_type
                bisect.insort_left(units, unit)

            # if in range: attack!
            if (unit.y, unit.x) in in_range:
                target_coords = {(t.y, t.x): t for t in targets}

                candidates = [
                    (hps[(y, x)], y, x)
                    for y, x in adjacent(unit.y, unit.x)
                    if (y, x) in target_coords
                ]
                _, target_y, target_x = min(candidates)

                target_unit = target_coords[(target_y, target_x)]
                hps[(target_y, target_x)] -= 3
                if hps[(target_y, target_x)] <= 0:
                    units.remove(target_unit)
                    del hps[(target_y, target_x)]
                    field[target_y][target_x] = '.'

        i += 1
        # print(f'@{i}')
        # print_field(field, hps, units)


SAMPLE1 = '''\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
'''

SAMPLE2 = '''\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
'''

SAMPLE3 = '''\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
'''

SAMPLE4 = '''\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
'''

SAMPLE5 = '''\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
'''

SAMPLE6 = '''\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE1, 27730),
        (SAMPLE2, 36334),
        (SAMPLE3, 39514),
        (SAMPLE4, 27755),
        (SAMPLE5, 28944),
        (SAMPLE6, 18740),
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
