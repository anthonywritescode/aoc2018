import argparse
import itertools
import re

import pytest

from support import timing

PATTERN = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')


def compute(s: str) -> int:
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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
