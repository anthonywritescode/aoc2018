import argparse
import string

import pytest


def reacted_length(s: str) -> int:
    s = s.strip()
    ret = [s[0]]
    for c in s[1:]:
        if ret and c == ret[-1].swapcase():
            ret.pop()
        else:
            ret.append(c)
    return len(ret)


def compute(s: str) -> int:
    return min(
        reacted_length(s.replace(c, '').replace(c.upper(), ''))
        for c in string.ascii_lowercase
    )


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('dabAcCaCBAcCcaDA', 4),
        ('dabAcCaCBAcCcaDA\n', 4),
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
