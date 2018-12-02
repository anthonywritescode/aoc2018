## advent of code 2018
### intro + project template

***

### what is advent of code

- "advent calendar" of programming challenges
- practice problem solving
- prepare for interviews
- etc.

***

### advent 2018

- my primary solutions will be in python
- other solutions in other languages (time permitting!)

***

### project template

- [pre-commit](https://pre-commit.com)
- [mypy](http://mypy-lang.org)
- [pytest](https://pytest.org)

***

### `.pre-commit-config.yaml`

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.0.0
    hooks:
    # ...
    -   id: flake8
# ...
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.641
    hooks:
    -   id: mypy
```

***

### `requirements.txt`

```
# ...
pre-commit
pytest
```

```console
$ virtualenv venv -ppython3
...

$ . venv/bin/activate

(venv) $ pip install -r requirements.txt
...

(venv) $ pre-commit install
pre-commit installed at .../.git/hooks/pre-commit
```

***

### `day*/part*.py`

```python
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0

if __name__ == '__main__':
    exit(main())
```

***

### `day*/part*.py`

```python
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        ('+1\n-2\n+3\n+1', 3),
        ('+1\n+1\n+1', 3),
        ('+1\n+1\n-2', 0),
        ('-1\n-2\n-3', -6),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected
```

***

### `day*/part*.py`

```python
import argparse

import pytest

def compute(s: str) -> int:
    # TODO: implement solution here!
    return 0
```

***

### testing

```pytest
$ pytest -q --tb=short day1/part1.py
FF.F                                                                 [100%]
================================= FAILURES =================================
__________________________ test[+1\n-2\n+3\n+1-3] __________________________
day1/part3.py:28: in test
    assert compute(input_s) == expected
E   AssertionError: assert 0 == 3
E    +  where 0 = compute('+1\n-2\n+3\n+1')
____________________________ test[+1\n+1\n+1-3] ____________________________
day1/part3.py:28: in test
    assert compute(input_s) == expected
E   AssertionError: assert 0 == 3
E    +  where 0 = compute('+1\n+1\n+1')
___________________________ test[-1\n-2\n-3--6] ____________________________
day1/part3.py:28: in test
    assert compute(input_s) == expected
E   AssertionError: assert 0 == -6
E    +  where 0 = compute('-1\n-2\n-3')
3 failed, 1 passed in 0.04 seconds
```

***

### challenge answer

Place the input at `day*/input.txt`.

```console
$ python day1/part1.py day1/input.txt
587
```

Repeat for part2!

***

### advent 2018

- I'll be live streaming my solutions on twitch:
  [anthonywritescode](https://twitch.tv/anthonywritescode)
- commiting them to github:
  [anthonywritescode/aoc2018](https://github.com/anthonywritescode/aoc2018)
- and of course uploading to youtube!
