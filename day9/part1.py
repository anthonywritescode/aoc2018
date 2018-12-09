import argparse
import collections
import itertools
import re
from typing import Optional
from typing import Tuple

import pytest

from support import timing

PATTERN = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')


def compute_list(s: str) -> int:
    match = PATTERN.match(s.strip())
    assert match, s
    player_count, max_marble = int(match.group(1)), int(match.group(2))

    current_marble = 0
    circle = [0]
    players = [0] * player_count

    for val, player_index in zip(
            range(1, max_marble + 1),
            itertools.cycle(range(player_count)),
    ):
        if val % 23 == 0:
            players[player_index] += val
            victim = current_marble = (current_marble - 7) % len(circle)
            players[player_index] += circle[victim]
            del circle[victim]
            current_marble = victim % len(circle)
        else:
            current_marble = (current_marble + 2) % len(circle)
            circle.insert(current_marble, val)
    return max(players)


def compute_deque(s: str) -> int:
    match = PATTERN.match(s.strip())
    assert match, s
    player_count, max_marble = int(match.group(1)), int(match.group(2))

    circle = collections.deque([0])
    players = [0] * player_count

    for val, player_index in zip(
            range(1, max_marble + 1),
            itertools.cycle(range(player_count)),
    ):
        if val % 23 == 0:
            players[player_index] += val
            circle.rotate(7)
            players[player_index] += circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(val)
    return max(players)


class Node:
    def __init__(
            self,
            val: int,
            left: Optional['Node'] = None,
            right: Optional['Node'] = None,
    ):
        self.val = val
        if left is None and right is None:
            self.left = self
            self.right = self
        else:
            assert left and right
            self.left, self.right = left, right
            # fix up the other sides
            self.left.right = self
            self.right.left = self

    def __repr__(self) -> str:
        values = []
        node = self
        while True:
            values.append(node.val)
            node = node.right
            if node is self:
                break
        beginning = values.index(min(values))
        values = values[beginning:] + values[:beginning]
        return f'{type(self).__name__}({self.val}, <{values}>)'

    def left_n(self, n: int) -> 'Node':
        node = self
        for _ in range(n):
            node = node.left
        return node

    def insert(self, val: int) -> 'Node':
        return Node(val, self, self.right)

    def remove(self) -> Tuple['Node', int]:
        self.left.right = self.right
        self.right.left = self.left
        return self.right, self.val


def compute(s: str) -> int:
    match = PATTERN.match(s.strip())
    assert match, s
    player_count, max_marble = int(match.group(1)), int(match.group(2))

    circle = Node(0)
    players = [0] * player_count

    for val, player_index in zip(
            range(1, max_marble + 1),
            itertools.cycle(range(player_count)),
    ):
        if val % 23 == 0:
            players[player_index] += val
            circle, val = circle.left_n(7).remove()
            players[player_index] += val
        else:
            circle = circle.right.insert(val)
    return max(players)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('9 players; last marble is worth 25 points', 32),
        ('10 players; last marble is worth 1618 points', 8317),
        ('13 players; last marble is worth 7999 points', 146373),
        ('17 players; last marble is worth 1104 points', 2764),
        ('21 players; last marble is worth 6111 points', 54718),
        ('30 players; last marble is worth 5807 points', 37305),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing('list'):
        print(compute_list(f.read()))

    with open(args.data_file) as f, timing('deque'):
        print(compute_deque(f.read()))

    with open(args.data_file) as f, timing('circular dlist'):
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
