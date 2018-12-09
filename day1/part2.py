import argparse
import itertools

import pytest

from support import timing


def compute_non_itertools(s: str) -> int:
    val = 0
    seen = {val}
    while True:
        for line in s.splitlines():
            val += int(line)
            if val in seen:
                return val
            else:
                seen.add(val)
    assert False, 'unreachable'


def compute(s: str) -> int:
    val = 0
    seen = {val}
    for line in itertools.cycle(s.splitlines()):
        val += int(line)
        if val in seen:
            return val
        else:
            seen.add(val)
    assert False, 'unreachable'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('+1\n-1', 0),
        ('+3\n+3\n+4\n-2\n-4', 10),
        ('-6\n+3\n+8\n+5\n-6', 5),
        ('+7\n+7\n-2\n-7\n-4', 14),

        # 0 -> 1 -> -1 -> 0
        ('+1\n-2', 0),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing('itertools'):
        print(compute(f.read()))
    with open(args.data_file) as f, timing('non itertools'):
        print(compute_non_itertools(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
