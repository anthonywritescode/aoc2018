import argparse

import pytest

from support import timing


def compute(s: str) -> str:
    n = int(s)
    recipes = [3, 7]
    e1_i = 0
    e2_i = 1

    while len(recipes) < n + 10:
        recipe_sum = recipes[e1_i] + recipes[e2_i]
        if recipe_sum >= 10:
            recipes.append(recipe_sum // 10)
        recipes.append(recipe_sum % 10)

        e1_i = (e1_i + 1 + recipes[e1_i]) % len(recipes)
        e2_i = (e2_i + 1 + recipes[e2_i]) % len(recipes)

    return ''.join(str(r) for r in recipes[n:n + 10])


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('5', '0124515891'),
        ('9', '5158916779'),
        ('18', '9251071085'),
        ('2018', '5941429882'),
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
