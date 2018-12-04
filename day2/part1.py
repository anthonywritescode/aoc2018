import argparse
import collections
import itertools
from typing import Counter

import pytest


def compute_orig(s: str) -> int:
    twos, threes = 0, 0
    for line in s.splitlines():  # O(N') N = number of lines
        char_counts = collections.Counter(line)  # O(N) N = length of s
        if 2 in char_counts.values():  # O(M) M is the unique characters in s
            twos += 1
        if 3 in char_counts.values():  # O(M) ...
            threes += 1
    return twos * threes


def compute_golf(s: str) -> int:
    count_counts = collections.Counter(itertools.chain.from_iterable([
        set(collections.Counter(line).values())
        for line in s.splitlines()
    ]))
    return count_counts[2] * count_counts[3]


def compute_char_subtract(s: str) -> int:
    twos = threes = 0
    for line in s.splitlines():
        line_list = list(line)
        for c in set(line_list):
            line_list.remove(c)
        two_plus = set(line_list)
        for c in two_plus:
            line_list.remove(c)
        three_plus = set(line_list)
        for c in three_plus:
            line_list.remove(c)
        four_plus = set(line_list)
        twos += bool(two_plus - three_plus)
        threes += bool(three_plus - four_plus)
    return twos * threes


def compute(s: str) -> int:
    count_counts: Counter[int] = collections.Counter()
    for line in s.splitlines():  # O(N') N = number of lines
        char_counts = collections.Counter(line)  # O(N) N = length of s
        unique_char_counts = set(char_counts.values())  # O(N) N = unique chars
        count_counts.update(unique_char_counts)  # O(N) N = unique counts
    return count_counts[2] * count_counts[3]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('', 0),
        ('aabbb', 1),
        (
            'abcdef\n'
            'bababc\n'
            'abbcde\n'
            'abcccd\n'
            'aabcdd\n'
            'abcdee\n'
            'ababab\n',
            12,
        ),
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
