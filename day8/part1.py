import argparse
from typing import Any
from typing import Callable
from typing import List
from typing import NamedTuple

import pytest


class Node(NamedTuple):
    # mypy doesn't yet support recursive types
    children: List[Any]
    metadata: List[int]


def make_node(values: List[int], cb: Callable[[int], None]) -> Node:
    node = Node([], [])

    children_count = values.pop()
    metadata_count = values.pop()

    for _ in range(children_count):
        node.children.append(make_node(values, cb))

    for _ in range(metadata_count):
        value = values.pop()
        cb(value)
        node.metadata.append(value)

    return node


def compute(s: str) -> int:
    values = list(reversed([int(p) for p in s.split()]))

    all_metadata: List[int] = []
    make_node(values, all_metadata.append)

    return sum(all_metadata)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2', 138),
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
