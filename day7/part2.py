import argparse
import bisect
import collections
from typing import DefaultDict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import pytest

from support import timing


def compute_orig(s: str, *, procs: int, duration: int) -> int:
    rdeps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    all_letters: Set[str] = set()

    for line in s.splitlines():
        p_from, p_to = line[5], line[36]
        rdeps[p_to].add(p_from)
        all_letters.update(p_from, p_to)

    t = 0
    workers: List[Optional[Tuple[int, str]]] = [None] * procs
    assignable = set(all_letters)

    while all_letters or any(workers):
        candidates = sorted(
            [k for k in assignable if len(rdeps[k]) == 0],
            reverse=True,
        )
        for i, v in enumerate(workers):
            if not candidates:
                break

            if v is None:
                c = candidates.pop()
                workers[i] = (t + duration + ord(c) - ord('A') + 1, c)
                assignable.remove(c)

        t = min(kv[0] for kv in workers if kv is not None)

        # reset any completed workers
        for i, val in enumerate(workers):
            if val is not None:
                vt, vc = val
                if vt == t:
                    workers[i] = None
                    all_letters.remove(vc)
                    for x in rdeps.values():
                        x.discard(vc)

    return t


def compute(s: str, *, procs: int, duration: int) -> int:
    deps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    rdeps: DefaultDict[str, Set[str]] = collections.defaultdict(set)
    all_letters: Set[str] = set()

    for line in s.splitlines():
        p_from, p_to = line[5], line[36]
        rdeps[p_to].add(p_from)
        deps[p_from].add(p_to)
        all_letters.update((p_from, p_to))

    i = 0
    no_deps = sorted([c for c in all_letters if c not in rdeps])
    workers: List[Tuple[int, str]] = []

    t = 0
    while i < len(no_deps) or workers:
        for j, _ in zip(range(i, len(no_deps)), range(procs - len(workers))):
            c = no_deps[j]
            i += 1
            work = (t + duration + ord(c) - ord('A') + 1, c)
            bisect.insort_left(workers, work)

        t = workers[0][0]
        while workers and workers[0][0] == t:
            removed = workers[0][1]
            del workers[0]
            for c in deps[removed]:
                rdeps[c].remove(removed)
                if not rdeps[c]:
                    bisect.insort_left(no_deps, c, i)
    return t


@pytest.mark.parametrize(
    ('input_s', 'procs', 'duration', 'expected'),
    (
        (
            'Step C must be finished before step A can begin.\n'
            'Step C must be finished before step F can begin.\n'
            'Step A must be finished before step B can begin.\n'
            'Step A must be finished before step D can begin.\n'
            'Step B must be finished before step E can begin.\n'
            'Step D must be finished before step E can begin.\n'
            'Step F must be finished before step E can begin.\n',

            2,
            0,

            15,
        ),
    ),
)
def test(input_s: str, procs: int, duration: int, expected: str) -> None:
    assert compute(input_s, procs=procs, duration=duration) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    parser.add_argument('--procs', default=5, type=int)
    parser.add_argument('--duration', default=60, type=int)
    args = parser.parse_args()

    with open(args.data_file) as f, timing('orig'):
        print(compute_orig(f.read(), procs=args.procs, duration=args.duration))

    with open(args.data_file) as f, timing('topo sort'):
        print(compute(f.read(), procs=args.procs, duration=args.duration))

    return 0


if __name__ == '__main__':
    exit(main())
