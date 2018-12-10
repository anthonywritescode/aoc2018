import argparse
import collections
from typing import DefaultDict
from typing import Set

import pytest

from support import timing


def compute_orig(s: str) -> str:
    rdeps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    all_letters: Set[str] = set()

    for line in s.splitlines():
        p_from, p_to = line[5], line[36]
        rdeps[p_to].add(p_from)
        all_letters.update((p_from, p_to))

    ret = ''
    while all_letters:
        candidates = [(len(rdeps[k]), k) for k in all_letters]
        _, answer = sorted(candidates)[0]
        ret += answer
        all_letters.remove(answer)
        for v in rdeps.values():
            v.discard(answer)

    return ret


def compute(s: str) -> str:
    deps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    rdeps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    all_letters: Set[str] = set()

    for line in s.splitlines():
        p_from, p_to = line[5], line[36]
        rdeps[p_to].add(p_from)
        deps[p_from].add(p_to)
        all_letters.update((p_from, p_to))

    no_deps = {c for c in all_letters if c not in rdeps}

    ret = ''
    while no_deps:
        removed = min(no_deps)
        ret += removed
        no_deps.remove(removed)
        for c in deps[removed]:
            rdeps[c].remove(removed)
            if not rdeps[c]:
                no_deps.add(c)
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

    with open(args.data_file) as f, timing('orig'):
        print(compute_orig(f.read()))

    with open(args.data_file) as f, timing('topo sort'):
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
