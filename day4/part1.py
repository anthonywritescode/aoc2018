import argparse
import collections
import random
import re
from typing import Counter
from typing import DefaultDict
from typing import List
from typing import NamedTuple
from typing import Tuple

import pytest

EVENT = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\]')
BEGIN_SHIFT = re.compile(rf'{EVENT.pattern} Guard #(\d+) begins shift$')


class Duration(NamedTuple):
    start: int
    end: int

    @property
    def time_asleep(self) -> int:
        return self.end - self.start


def total_asleep_time(kv: Tuple[int, List[Duration]]) -> int:
    return sum(event.time_asleep for event in kv[1])


def compute(s: str) -> int:
    guard = start = -1
    by_guard: DefaultDict[int, List[Duration]] = collections.defaultdict(list)

    for line in sorted(s.splitlines()):
        begin_shift_match = BEGIN_SHIFT.match(line)
        event_match = EVENT.match(line)
        assert event_match, line
        if begin_shift_match:
            guard = int(begin_shift_match.group(2))
        elif start == -1:
            start = int(event_match.group(1))
        else:
            by_guard[guard].append(Duration(start, int(event_match.group(1))))
            start = -1

    sleepiest, durations = sorted(by_guard.items(), key=total_asleep_time)[-1]

    asleep_times: Counter[int] = collections.Counter()
    for duration in durations:
        asleep_times.update(range(duration.start, duration.end))

    (sleepiest_minute, _), = asleep_times.most_common(1)
    return sleepiest * sleepiest_minute


SAMPLE_INPUT = '''\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, 240),
        (
            # input is unordered
            ''.join(random.sample(
                SAMPLE_INPUT.splitlines(True),
                k=len(SAMPLE_INPUT.splitlines()),
            )),
            240,
        ),
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
