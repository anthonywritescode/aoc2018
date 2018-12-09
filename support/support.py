import contextlib
import time
from typing import Generator
from typing import Sequence
from typing import Tuple
from typing import TypeVar

T = TypeVar('T')


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}')


def every_other(seq: Sequence[T]) -> Generator[Tuple[T, T], None, None]:
    length = len(seq)
    for i, el in enumerate(seq):
        for j in range(i + 1, length):
            yield el, seq[j]
