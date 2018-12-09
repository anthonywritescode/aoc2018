import argparse
from typing import Any
from typing import List
from typing import NamedTuple
from typing import Optional

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


def compute_recursive(s: str) -> int:
    values = list(reversed([int(p) for p in s.split()]))

    root = make_node(values)
    return root.value()


def compute(s: str) -> int:
    children_children_stack: List[List[int]] = [[]]
    orig_children_left_stack = [1]
    children_left_stack = [1]
    metadata_left_stack = [0]
    child_count: Optional[int] = None
    current_total = 0

    for x in s.split():
        val = int(x)

        if not children_left_stack[-1] and not metadata_left_stack[-1]:
            children_children_stack.pop()
            orig_children_left_stack.pop()
            children_left_stack.pop()
            metadata_left_stack.pop()
            children_children_stack[-1].append(current_total)
            current_total = 0

        if children_left_stack[-1]:
            if child_count is None:
                child_count = val
            else:
                children_left_stack[-1] -= 1

                children_children_stack.append([])
                children_left_stack.append(child_count)
                orig_children_left_stack.append(child_count)
                metadata_left_stack.append(val)

                child_count = None
        elif children_left_stack[-1] == 0 and metadata_left_stack[-1]:
            metadata_left_stack[-1] -= 1
            if orig_children_left_stack[-1]:
                val -= 1
                if val >= 0:
                    try:
                        current_total += children_children_stack[-1][val]
                    except IndexError:
                        pass
            else:
                current_total += val
        else:
            raise AssertionError('unreachable!')

    return current_total


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
