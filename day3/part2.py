import argparse
import re
from typing import NamedTuple

import pytest

from support import timing


PATTERN = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int

    @classmethod
    def parse(cls, s: str) -> 'Claim':
        match = PATTERN.match(s)
        assert match, s
        return cls(*[int(g) for g in match.groups()])

    def overlaps(self, other: 'Claim') -> bool:
        """rectangle collision detection"""
        return (
            self.left < other.left + other.width and
            self.left + self.width > other.left and
            self.top < other.top + other.height and
            self.top + self.height > other.top
        )


def compute(s: str) -> int:
    claims = [Claim.parse(line) for line in s.splitlines()]

    for claim in claims:
        for other_claim in claims:
            if claim != other_claim and claim.overlaps(other_claim):
                break
        else:
            return claim.id

    raise AssertionError('unreachable!')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            '#1 @ 1,3: 4x4\n'
            '#2 @ 3,1: 4x4\n'
            '#3 @ 5,5: 2x2\n',

            3,
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
