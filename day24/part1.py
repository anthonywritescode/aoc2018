import argparse
import re
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Set
from typing import Tuple

import pytest

from support import timing

GROUP_RE = re.compile(
    r'(\d+) units each with (\d+) hit points '
    r'(?:\(([^)]+)\) )?with an attack that '
    r'does (\d+) (\w+) damage at initiative (\d+)'
)


class Group(NamedTuple):
    priority: int
    units: int
    hp: int
    weak_types: FrozenSet[str]
    immune_types: FrozenSet[str]
    attack: int
    attack_type: str

    @property
    def effective_power(self) -> int:
        return self.attack * self.units

    @property
    def sort_key(self) -> Tuple[int, int]:
        return (-1 * self.effective_power, -1 * self.priority)

    def damage(self, target: 'Group') -> int:
        if self.attack_type in target.immune_types:
            return 0
        elif self.attack_type in target.weak_types:
            return 2 * self.effective_power
        else:
            return self.effective_power

    def receive_attack(self, attacker: 'Group') -> 'Group':
        units_lost = attacker.damage(self) // self.hp
        return self._replace(units=max(0, self.units - units_lost))

    @classmethod
    def parse(cls, s: str) -> 'Group':
        match = GROUP_RE.match(s)
        assert match, s

        (
            units_s, hp_s, resistances_s, attack_s, attack_type, priority_s,
        ) = match.groups()

        resistances: Dict[str, FrozenSet[str]]
        resistances = {'weak': frozenset(), 'immune': frozenset()}
        if resistances_s:
            for part in resistances_s.split('; '):
                target, _, types_list = part.split(' ', 2)
                resistances[target] = frozenset(types_list.split(', '))

        return cls(
            priority=int(priority_s),
            units=int(units_s),
            hp=int(hp_s),
            weak_types=resistances['weak'],
            immune_types=resistances['immune'],
            attack=int(attack_s),
            attack_type=attack_type,
        )


def get_targets(a1: List[Group], a2: List[Group]) -> Dict[int, int]:
    targets: Dict[int, int] = {}
    seen: Set[int] = set()

    for g in a1:
        target: Optional[Group] = None
        damage = 0

        for cand in a2:
            if cand.priority in seen:
                continue
            cand_damage = g.damage(cand)
            if cand_damage > damage:
                target = cand
                damage = cand_damage

        if target is not None:
            targets[g.priority] = target.priority
            seen.add(target.priority)

    return targets


def compute(s: str) -> int:
    a1_s, a2_s = s.split('\n\n')
    a1 = [Group.parse(s) for s in a1_s.splitlines()[1:]]
    a2 = [Group.parse(s) for s in a2_s.splitlines()[1:]]
    a1 = sorted(a1, key=lambda g: g.sort_key)
    a2 = sorted(a2, key=lambda g: g.sort_key)

    while a1 and a2:
        # target selection
        targets_a1 = get_targets(a1, a2)
        targets_a2 = get_targets(a2, a1)

        # attacking
        all_things = sorted(
            [(g.priority, targets_a1, a1, a2) for g in a1] +
            [(g.priority, targets_a2, a2, a1) for g in a2],
            key=lambda g_targets_l: -1 * g_targets_l[0],
        )
        for g_priority, targets, this_l, other_l in all_things:
            if g_priority in targets:
                g, = [g for g in this_l if g.priority == g_priority]
                ind, = [
                    i for i, other in enumerate(other_l)
                    if other.priority == targets[g_priority]
                ]
                other_l[ind] = other_l[ind].receive_attack(g)

        a1 = sorted([g for g in a1 if g.units], key=lambda g: g.sort_key)
        a2 = sorted([g for g in a2 if g.units], key=lambda g: g.sort_key)

    return sum(g.units for g in a1 + a2)


SAMPLE_INPUT = '''\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
'''  # noqa: E501


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE_INPUT, 5216),
    ),
)
def test(input_s: str, expected: int) -> None:
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
