import argparse
import collections
import itertools
import re
from typing import Optional
from typing import Tuple

import pytest

from support import timing

PATTERN = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')


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


def compute_dlist(s: str) -> int:
    match = PATTERN.match(s.strip())
    assert match, s
    player_count, max_marble = int(match.group(1)), int(match.group(2))

    max_marble *= 100

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


def compute(s: str) -> int:
    match = PATTERN.match(s.strip())
    assert match, s
    player_count, max_marble = int(match.group(1)), int(match.group(2))

    max_marble *= 100

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


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    # no sample inputs given
    (),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing('circular dlist'):
        print(compute_dlist(f.read()))

    with open(args.data_file) as f, timing('deque'):
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
