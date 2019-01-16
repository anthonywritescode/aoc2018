import argparse
import re
from typing import Any
from typing import NamedTuple

import pytest
from z3 import If
from z3 import Int
from z3 import Optimize
from z3 import Sum

from support import timing

INT = re.compile(r'-?\d+')


def rotated_squares_collide(
        x1: int, y1: int, r1: int,
        x2: int, y2: int, r2: int,
) -> bool:
    axis1_x, axis1_y = (1, 1)

    box1_top_proj1 = axis1_x * x1 + axis1_y * (y1 + r1)
    box1_bot_proj1 = axis1_x * x1 + axis1_y * (y1 - r1)
    box1_proj1_min = min(box1_top_proj1, box1_bot_proj1)
    box1_proj1_max = max(box1_top_proj1, box1_bot_proj1)

    box2_top_proj1 = axis1_x * x2 + axis1_y * (y2 + r2)
    box2_bot_proj1 = axis1_x * x2 + axis1_y * (y2 - r2)
    box2_proj1_min = min(box2_top_proj1, box2_bot_proj1)
    box2_proj1_max = max(box2_top_proj1, box2_bot_proj1)

    overlap_proj1 = (
        box1_proj1_max >= box2_proj1_min and
        box2_proj1_max >= box1_proj1_min
    )

    axis2_x, axis2_y = (-1, 1)

    box1_top_proj2 = axis2_x * x1 + axis2_y * (y1 + r1)
    box1_bot_proj2 = axis2_x * x1 + axis2_y * (y1 - r1)
    box1_proj2_min = min(box1_top_proj2, box1_bot_proj2)
    box1_proj2_max = max(box1_top_proj2, box1_bot_proj2)

    box2_top_proj2 = axis2_x * x2 + axis2_y * (y2 + r2)
    box2_bot_proj2 = axis2_x * x2 + axis2_y * (y2 - r2)
    box2_proj2_min = min(box2_top_proj2, box2_bot_proj2)
    box2_proj2_max = max(box2_top_proj2, box2_bot_proj2)

    overlap_proj2 = (
        box1_proj2_max >= box2_proj2_min and
        box2_proj2_max >= box1_proj2_min
    )

    return overlap_proj1 and overlap_proj2


class Bot(NamedTuple):
    x: int
    y: int
    z: int
    r: int

    @classmethod
    def parse(cls, s: str) -> 'Bot':
        return cls(*[int(p) for p in INT.findall(s)])

    def collides(self, other: 'Bot') -> bool:
        return (
            rotated_squares_collide(
                self.x, self.y, self.r,
                other.x, other.y, other.r,
            ) and
            rotated_squares_collide(
                self.x, self.z, self.r,
                other.x, other.z, other.r,
            ) and
            rotated_squares_collide(
                self.y, self.z, self.r,
                other.y, other.z, other.r,
            )
        )


def zabs(expr: Any) -> If:
    return If(expr > 0, expr, -expr)


def compute(s: str) -> int:
    bots = [Bot.parse(line) for line in s.splitlines()]

    x, y, z = Int('x'), Int('y'), Int('z')
    dist = Int('dist')
    sum_var = Int('sum_var')
    in_range_vars = []

    o = Optimize()
    for i, bot in enumerate(bots):
        in_range = Int(f'in_range_{i}')
        o.add(
            in_range ==
            If(
                zabs(x - bot.x) + zabs(y - bot.y) + zabs(z - bot.z) <= bot.r,
                1,
                0,
            )
        )
        in_range_vars.append(in_range)
    o.add(sum_var == Sum(in_range_vars))
    o.add(dist == zabs(x) + zabs(y) + zabs(z))

    o.maximize(sum_var)
    o.minimize(dist)

    o.check()
    m = o.model()

    return m[dist].as_long()


SAMPLE_INPUT = '''\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, 36),
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
