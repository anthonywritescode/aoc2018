import argparse
import bisect
import enum
from typing import List
from typing import NamedTuple

import pytest

from support import timing


DIRECTION_TO_COORDS = {
    'v': (1, 0),
    '^': (-1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


class TurnDirection(enum.Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


TURNS = {
    ('v', '|'): 'v',
    ('^', '|'): '^',
    ('>', '-'): '>',
    ('<', '-'): '<',

    ('v', '\\'): '>',
    ('v', '/'): '<',
    ('^', '\\'): '<',
    ('^', '/'): '>',

    ('>', '\\'): 'v',
    ('>', '/'): '^',
    ('<', '\\'): '^',
    ('<', '/'): 'v',
}

INTERSECTION_TURNS = {
    ('<', TurnDirection.LEFT): 'v',
    ('<', TurnDirection.STRAIGHT): '<',
    ('<', TurnDirection.RIGHT): '^',

    ('>', TurnDirection.LEFT): '^',
    ('>', TurnDirection.STRAIGHT): '>',
    ('>', TurnDirection.RIGHT): 'v',

    ('^', TurnDirection.LEFT): '<',
    ('^', TurnDirection.STRAIGHT): '^',
    ('^', TurnDirection.RIGHT): '>',

    ('v', TurnDirection.LEFT): '>',
    ('v', TurnDirection.STRAIGHT): 'v',
    ('v', TurnDirection.RIGHT): '<',
}
NEXT_TURN = {
    TurnDirection.LEFT: TurnDirection.STRAIGHT,
    TurnDirection.STRAIGHT: TurnDirection.RIGHT,
    TurnDirection.RIGHT: TurnDirection.LEFT,
}


class Cart(NamedTuple):
    y: int
    x: int
    direction: str
    next_turn: TurnDirection = TurnDirection.LEFT

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Cart):
            return NotImplemented
        else:
            return (self.y, self.x) < (other.y, other.x)

    def update(self, track: List[List[str]]) -> 'Cart':
        change_y, change_x = DIRECTION_TO_COORDS[self.direction]
        new_y, new_x = self.y + change_y, self.x + change_x

        lands_on = track[new_y][new_x]
        if lands_on == '+':
            direction = INTERSECTION_TURNS[(self.direction, self.next_turn)]
            next_turn = NEXT_TURN[self.next_turn]
            return self._replace(
                y=new_y, x=new_x, direction=direction, next_turn=next_turn,
            )
        else:
            direction = TURNS[(self.direction, lands_on)]
            return self._replace(y=new_y, x=new_x, direction=direction)


def print_track(track: List[List[str]], carts: List[Cart]) -> None:
    track = [row.copy() for row in track]
    for cart in carts:
        track[cart.y][cart.x] = cart.direction
    print('\n'.join(''.join(line) for line in track))


def compute(s: str) -> str:
    track = [list(line) for line in s.splitlines()]
    carts: List[Cart] = []

    for y, row in enumerate(track):
        for x, c in enumerate(row):
            if c in '<>^v':
                carts.append(Cart(y, x, c))
                if c in '<>':
                    track[y][x] = '-'
                else:
                    track[y][x] = '|'

    while True:
        for cart in tuple(carts):
            carts.remove(cart)
            new_cart = cart.update(track)
            insert_point = bisect.bisect_left(carts, new_cart)
            if (
                    insert_point < len(carts) and
                    carts[insert_point].x == new_cart.x and
                    carts[insert_point].y == new_cart.y
            ):
                return f'{new_cart.x},{new_cart.y}'
            carts.insert(insert_point, new_cart)


T1 = '''\
|
v
|
|
|
^
|
'''

T2 = '\n'.join((
    r'/->-\         ',
    r'|   |  /----\ ',
    r'| /-+--+-\  | ',
    r'| | |  | v  | ',
    r'\-+-/  \-+--/ ',
    r'  \------/    ',
))


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (T1, '0,3'),
        (T2, '7,3'),
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
