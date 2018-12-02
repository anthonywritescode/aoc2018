import argparse
from typing import Set

import pytest


def compute_orig(s: str) -> str:  # O(N^2 * M)
    lines = s.splitlines()
    for line in lines:  # O(N)
        for other_line in lines:  # O(N)
            assert len(line) == len(other_line), (line, other_line)
            ret = ''
            for c1, c2 in zip(line, other_line):  # O(M)
                if c1 == c2:
                    ret += c1
            if len(ret) == len(line) - 1:
                return ret
    raise AssertionError('unreachable!')


def _to_substrings(s: str) -> Set[str]:  # O(M) work + O(M) space
    """bar => {'ar', 'br', 'ba'}"""
    return {s[:i] + s[i + 1:] for i in range(len(s))}


def compute(s: str) -> str:  # O(N * M)
    seen: Set[str] = set()

    for line in s.splitlines():  # O(N)
        new_substrings = _to_substrings(line)
        already_seen = new_substrings & seen  # O(M)
        if already_seen:
            answer, = already_seen
            return answer
        else:
            seen.update(new_substrings)  # O(N * M) space
    else:
        raise AssertionError('unreachable!')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('', set()),
        ('a', {''}),
        ('bar', {'ar', 'br', 'ba'}),
        ('foo', {'oo', 'fo'}),
    ),
)
def test_to_substrings(input_s: str, expected: Set[str]) -> None:
    assert _to_substrings(input_s) == expected


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
