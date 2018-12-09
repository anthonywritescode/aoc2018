import argparse
import difflib
from typing import Set

import pytest

from support import every_other
from support import timing


def compute_orig(s: str) -> str:  # O(N^2 * M)
    lines = s.splitlines()
    for line, other_line in every_other(lines):  # O(N^2)
        assert len(line) == len(other_line), (line, other_line)
        ret = ''
        for c1, c2 in zip(line, other_line):  # O(M)
            if c1 == c2:
                ret += c1
        if len(ret) == len(line) - 1:
            return ret
    raise AssertionError('unreachable!')


def compute_difflib(s: str) -> str:
    """does not work for len(line) < 3"""
    lines = s.splitlines(True)
    for line, other_line in every_other(lines):
        diffs = tuple(difflib.ndiff((line,), (other_line,)))
        if len(diffs) != 4:
            continue
        context_line = diffs[-1]
        if context_line.count('^') == 1 and '+' not in context_line:
            i = context_line.index('^')
            return diffs[0][:i].lstrip('- ') + diffs[0][i + 1:].strip()
    raise AssertionError('unreachable!')


def compute_sort(s: str) -> str:  # O(N * log(N) + O(N) * O(M))
    """does not always work, see test cases"""
    lines = sorted(s.splitlines())  # O(N * log(N))
    for line, other_line in zip(lines, lines[1:]):  # O(N)
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
        for substr in _to_substrings(line):  # O(M)
            if substr in seen:
                return substr
            else:
                seen.add(substr)
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
        # compute_difflib fails this test case, it can't handle strings < 3
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
        # maybe not a valid testcase, the problem only has a unique solution
        # the compute_sort fails this testcase
        ('zaa\nyaa\nabb\nbbb\n', 'aa'),
        # compute_sort fails this
        ('zaa\nbaa\nbbb', 'aa'),
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

    with open(args.data_file) as f, timing('substrings'):
        print(compute(f.read()))
    with open(args.data_file) as f, timing('difflib'):
        print(compute_difflib(f.read()))
    with open(args.data_file) as f, timing('orig'):
        print(compute_orig(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
