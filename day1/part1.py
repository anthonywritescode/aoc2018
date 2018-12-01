import argparse

import pytest


def compute_for_loop(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        val = int(line)
        ret += val
    return ret


def compute(s: str) -> int:
    return sum(int(line) for line in s.splitlines())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('+1\n-2\n+3\n+1', 3),
        ('+1\n+1\n+1', 3),
        ('+1\n+1\n-2', 0),
        ('-1\n-2\n-3', -6),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
