import argparse
from typing import Any
from typing import Callable
from typing import List
from typing import NamedTuple
from typing import Optional

import pytest

from support import timing


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


def compute_recursive(s: str) -> int:
    values = list(reversed([int(p) for p in s.split()]))

    all_metadata: List[int] = []
    make_node(values, all_metadata.append)

    return sum(all_metadata)


def compute(s: str) -> int:
    total = 0
    children_left_stack = [1]
    metadata_left_stack = [0]
    child_count: Optional[int] = None

    for x in s.split():
        val = int(x)

        if not children_left_stack[-1] and not metadata_left_stack[-1]:
            children_left_stack.pop()
            metadata_left_stack.pop()

        if children_left_stack[-1]:
            if child_count is None:
                child_count = val
            else:
                children_left_stack[-1] -= 1
                children_left_stack.append(child_count)
                metadata_left_stack.append(val)
                child_count = None
        elif children_left_stack[-1] == 0 and metadata_left_stack[-1]:
            metadata_left_stack[-1] -= 1
            total += val
        else:
            raise AssertionError('unreachable!')

    return total


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

    with open(args.data_file) as f, timing('iterative'):
        print(compute(f.read()))
    with open(args.data_file) as f, timing('recursive'):
        print(compute_recursive(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
