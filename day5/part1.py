import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    s = s.strip()
    ret = [s[0]]
    for c in s[1:]:
        if ret and c == ret[-1].swapcase():
            ret.pop()
        else:
            ret.append(c)
    return len(ret)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('dabAcCaCBAcCcaDA', 10),
        ('dabAcCaCBAcCcaDA\n', 10),
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
