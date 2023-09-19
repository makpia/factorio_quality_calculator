

from itertools import product

from quality import quality_status


def main():

    qs = quality_status(
        target_ge=2,
        upgrade_ratio=0.1,
        enrich_rate=1.4,
        ins=[1, 0, 0, 0, 0],
        tech_level=5,
    )

    result = qs.approximate()

    print(f'result of {qs = }')
    print(f'- {result.outs = }')
    print(f'- {sum(result.outs) = }')
    print()

    for upgrade_ratio, enrich_rate in product(
        (0.04, 0.06, 0.1, 0.25),
        (1, 1.16, 1.24, 1.4, 2),
    ):
        qs = quality_status(
            target_ge=2,
            upgrade_ratio=upgrade_ratio,
            enrich_rate=enrich_rate,
            ins=[1, 0, 0, 0, 0],
            tech_level=5,
        )
        result = qs.approximate()

        print(f'result of {qs = }')
        print(f'- {result.outs = }')
        print(f'- {sum(result.outs) = }')
        print()


if __name__ == '__main__':
    main()
