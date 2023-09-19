

from typing import Self

from dataclasses import dataclass, field


def _upgrade_rates(upgrade_ratio: float, level: int) -> list[float]:

    res = [0.] * (level - 1) + [
        upgrade_ratio ** k for k in range(5 - level + 1)]
    res[level - 1] -= sum(res[level:])

    return res


@dataclass(slots=True, frozen=True)
class quality_status:
    """
    - assemble
        - i1 -> a1 * o1 + a2 * o2 + a3 * o3 + ...
        - i2 -> b * o2
    - recycle
        - o1 -> a1 * i1 + a2 * i2 + a3 * i3 + ...
    """
    target_ge: int

    upgrade_ratio: float
    enrich_rate: float

    ins: list[float]
    outs: list[float] = field(
        default_factory=lambda: [0.] * 5,
        repr=False,
    )

    tech_level: int = 5  # not implemented yet

    def __post_init__(self) -> None:

        assert 0 < self.upgrade_ratio <= 1
        assert 1 <= self.enrich_rate
        assert self.target_ge in range(1, 6)
        assert self.tech_level >= self.target_ge
        assert len(self.ins) == 5
        assert len(self.outs) == 5

    def __str__(self) -> str:

        return '\n'.join([
            'in: ' + ', '.join([f'{i:.3f}' for i in self.ins]),
            'out: ' + ', '.join([f'{o:.3f}' for o in self.outs]),
        ])

    def _assemble(self) -> Self:

        outs = list(self.outs)

        for level in range(1, 5):
            if level < self.target_ge:
                outs = [
                    o + self.ins[level - 1] * r
                    for o, r in zip(
                        list(outs), _upgrade_rates(self.upgrade_ratio, level))
                ]
            else:
                outs[level - 1] += self.ins[level - 1] * self.enrich_rate

        outs[4] += self.ins[4] * self.enrich_rate

        return quality_status(
            self.target_ge,
            self.upgrade_ratio,
            self.enrich_rate,
            [0.] * 5,
            outs,
            self.tech_level,
        )

    def _recycle(self) -> Self:

        ins = list(self.ins)
        outs = list(self.outs)

        for i in range(4):
            if i + 1 < self.target_ge:
                ins = [
                    ini + outs[i] * r / 4
                    for ini, r in zip(
                        ins, _upgrade_rates(self.upgrade_ratio, i + 1))
                ]
                outs[i] = 0
            else:
                pass

        return quality_status(
            self.target_ge,
            self.upgrade_ratio,
            self.enrich_rate,
            ins,
            outs,
            self.tech_level,
        )

    def approximate(self) -> Self:

        res = self

        count = 0
        while True:
            res = res._assemble()
            count += 1
            if not res.outs[self.target_ge - 2] > 0 or count > 10000:
                break
            res = res._recycle()

        print(f'iterate times: {count}')

        return res
