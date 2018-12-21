import argparse
from typing import Set

import pytest

from support import timing


def compute(s: str) -> int:
    """Code was determined empirically using day21/genc.py"""
    prev_seen = -1
    seen: Set[int] = set()

    reg2 = reg3 = reg4 = 0

    while True:
        reg2 = reg3 | 65536
        reg3 = 1505483

        while True:
            reg4 = reg2 & 255
            reg3 = reg3 + reg4
            reg3 = reg3 & 16777215
            reg3 = reg3 * 65899
            reg3 = reg3 & 16777215
            if 256 <= reg2:
                reg2 //= 256
                continue
            else:
                break

        if reg3 in seen:
            return prev_seen
        else:
            prev_seen = reg3
            seen.add(prev_seen)


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
