import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    sequence = [int(c) for c in s.strip()]

    recipes = [3, 7]
    e1_i = 0
    e2_i = 1

    min_search = 0
    while True:
        recipe_sum = recipes[e1_i] + recipes[e2_i]
        if recipe_sum >= 10:
            recipes.append(recipe_sum // 10)
        recipes.append(recipe_sum % 10)

        e1_i = (e1_i + 1 + recipes[e1_i]) % len(recipes)
        e2_i = (e2_i + 1 + recipes[e2_i]) % len(recipes)

        i = min_search
        for i in range(min_search, len(recipes) - len(sequence)):
            if recipes[i:i + len(sequence)] == sequence:
                return i
        else:
            min_search = i


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('51589', 9),
        ('01245', 5),
        ('92510', 18),
        ('59414', 2018),
    ),
)
def test(input_s: str, expected: str) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
