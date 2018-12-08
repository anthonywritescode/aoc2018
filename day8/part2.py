import argparse
from typing import Any
from typing import List
from typing import NamedTuple

import pytest


class Node(NamedTuple):
    # mypy doesn't yet support recursive types
    children: List[Any]
    metadata: List[int]

    def value(self) -> int:
        if not self.children:
            return sum(self.metadata)
        else:
            ret = 0
            for ind in self.metadata:
                ind -= 1
                if ind < 0:
                    continue
                try:
                    ret += self.children[ind].value()
                except IndexError:  # non-existent indices are skipped
                    pass
            return ret


def make_node(values: List[int]) -> Node:
    node = Node([], [])

    children_count = values.pop()
    metadata_count = values.pop()

    for _ in range(children_count):
        node.children.append(make_node(values))

    for _ in range(metadata_count):
        node.metadata.append(values.pop())

    return node


def compute(s: str) -> int:
    values = list(reversed([int(p) for p in s.split()]))

    root = make_node(values)
    return root.value()


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2', 66),
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
