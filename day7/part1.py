import argparse
from typing import List
from typing import Set
from typing import Tuple

import pytest


def compute(s: str) -> str:
    deps: List[Tuple[str, str]] = []
    all_letters: Set[str] = set()

    for line in s.splitlines():
        p_from, p_to = line[5], line[36]
        deps.append((p_from, p_to))
        all_letters.update(p_from, p_to)

    ret = ''
    while all_letters:
        candidates = []

        for c in all_letters:
            if sum(1 for _, c2 in deps if c2 == c) == 0:
                candidates.append(c)

        answer = sorted(candidates)[0]
        ret += answer
        all_letters.remove(answer)
        deps = [(p_from, p_to) for p_from, p_to in deps if p_from != answer]

    return ret


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (
            'Step C must be finished before step A can begin.\n'
            'Step C must be finished before step F can begin.\n'
            'Step A must be finished before step B can begin.\n'
            'Step A must be finished before step D can begin.\n'
            'Step B must be finished before step E can begin.\n'
            'Step D must be finished before step E can begin.\n'
            'Step F must be finished before step E can begin.\n',

            'CABDFE',
        ),
    ),
)
def test(input_s: str, expected: str) -> None:
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
