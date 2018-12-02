import argparse

import pytest


def compute(s: str) -> str:
    lines = s.splitlines()
    for line in lines:
        for other_line in lines:
            assert len(line) == len(other_line), (line, other_line)
            ret = ''
            for c1, c2 in zip(line, other_line):
                if c1 == c2:
                    ret += c1
            if len(ret) == len(line) - 1:
                return ret
    raise AssertionError('unreachable!')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('a\nb\n', ''),
        (
            'abcde\n'
            'fghij\n'
            'klmno\n'
            'pqrst\n'
            'fguij\n'
            'axcye\n'
            'wvxyz\n',

            'fgij',
        ),
    ),
)
def test(input_s: str, expected: str) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    'input_s',
    (
        '',
        'foo\nbar\n',
    ),
)
def test_error(input_s: str) -> None:
    with pytest.raises(AssertionError) as excinfo:
        compute(input_s)
    assert excinfo.value.args == ('unreachable!',)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
